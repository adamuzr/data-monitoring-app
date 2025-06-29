import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_monitoring_app.settings')
django.setup()

import json
import datetime
from django.conf import settings
import psycopg2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_DIR, 'rules.json')
ALERTS_PATH = os.path.join(BASE_DIR, 'alerts.json')

def get_db_connection():
    db = settings.DATABASES['default']
    return psycopg2.connect(
        dbname=db['NAME'],
        user=db['USER'],
        password=db['PASSWORD'],
        host=db['HOST'],
        port=db['PORT'],
    )

def check_rule(conn, rule):
    table = rule['table']
    threshold = rule['threshold']
    row_count = rule['row_count']

    sql = f"SELECT COUNT(*) FROM {table}"
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            count = cur.fetchone()[0]
        except Exception as e:
            return f"Error querying table '{table}': {e}"

        if threshold == '<' and count < row_count:
            return f"Row count in '{table}' is less than {row_count} ({count} rows)"
        elif threshold == '>' and count > row_count:
            return f"Row count in '{table}' is greater than {row_count} ({count} rows)"
        elif threshold == '=' and count == row_count:
            return f"Row count in '{table}' equals {row_count} ({count} rows)"
    return None

def check_data_modification(conn, table, attribute=None, minutes=5):
    timestamp_col = attribute if attribute else 'last_update'
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"SELECT COUNT(*) FROM {table} WHERE {timestamp_col} >= NOW() - INTERVAL '{int(minutes)} minutes';"
            )
            count = cur.fetchone()[0]
            if count > 0:
                return f"{count} row(s) in '{table}' modified in the last {minutes} minutes (checked column: {timestamp_col})."
        except Exception as e:
            return f"Error checking modifications in '{table}.{timestamp_col}': {e}"
    return None

def check_unique_attribute(conn, rule):
    """
    Checks for duplicate values in the unique_attribute column.
    If watch_value is set, only checks for duplicates of that value.
    """
    table = rule['table']
    unique_attr = rule.get('unique_attribute')
    watch_value = rule.get('watch_value')
    if unique_attr:
        with conn.cursor() as cur:
            try:
                if watch_value:
                    # Only check for duplicates of the specific value
                    cur.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE {unique_attr} = %s", [watch_value]
                    )
                    count = cur.fetchone()[0]
                    if count > 1:
                        return f"Duplicate value '{watch_value}' found {count} times in '{table}.{unique_attr}'."
                else:
                    # Check for any duplicates
                    cur.execute(
                        f"SELECT {unique_attr}, COUNT(*) FROM {table} GROUP BY {unique_attr} HAVING COUNT(*) > 1"
                    )
                    duplicates = cur.fetchall()
                    if duplicates:
                        dup_values = ', '.join(str(row[0]) for row in duplicates)
                        return f"Duplicate values found in '{table}.{unique_attr}': {dup_values}"
            except Exception as e:
                return f"Error checking duplicates in '{table}.{unique_attr}': {e}"
    return None

def check_rules_and_generate_alerts():
    with open(RULES_PATH) as f:
        rules = json.load(f)
    try:
        with open(ALERTS_PATH) as f:
            alerts = json.load(f)
    except FileNotFoundError:
        alerts = []

    conn = get_db_connection()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for rule in rules:
        if not rule.get('is_active'):
            continue

        details_list = []

        # Row count check
        row_count_detail = check_rule(conn, rule)
        if row_count_detail:
            details_list.append(row_count_detail)

        # Data modification check
        if rule.get('check_modification'):
            minutes = rule.get('minutes', 5)
            mod_detail = check_data_modification(conn, rule['table'], rule.get('attribute', None), minutes)
            if mod_detail:
                details_list.append(mod_detail)

        # Duplicate check
        if rule.get('unique_attribute') and not rule.get('watch_value'):
            dup_detail = check_unique_attribute(conn, rule)
            if dup_detail:
                details_list.append(dup_detail)
        elif rule.get('unique_attribute') and rule.get('watch_value'):
            dup_detail = check_unique_attribute(conn, rule)
            if dup_detail:
                details_list.append(dup_detail)

        # Only create alert if any details exist
        if details_list:
            alert = {
                "alert_name": f"{rule['rule_name']} triggered",
                "rule_name": rule['rule_name'],
                "table": rule['table'],
                "row_count": rule.get('row_count', ''),
                "threshold": rule.get('threshold', ''),
                "created_at": now,
                "severity": rule.get('severity', 'Medium'),
                "details": details_list,  # Store as a list
                "status": "Active"
            }
            alerts.append(alert)

    conn.close()

    with open(ALERTS_PATH, 'w') as f:
        json.dump(alerts, f, indent=4)

if __name__ == "__main__":
    check_rules_and_generate_alerts()