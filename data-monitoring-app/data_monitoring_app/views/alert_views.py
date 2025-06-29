import json
import os
from django.conf import settings
from django.shortcuts import render, redirect

RULES_PATH = os.path.join(settings.BASE_DIR, 'data_monitoring_app', 'rules.json')
ALERTS_PATH = os.path.join(settings.BASE_DIR, 'data_monitoring_app', 'alerts.json')
PAST_ALERTS_PATH = os.path.join(settings.BASE_DIR, 'data_monitoring_app', 'past_alerts.json')

def alert_list(request):
    with open(RULES_PATH) as f:
        rules = json.load(f)
    try:
        with open(ALERTS_PATH) as f:
            alerts = json.load(f)
    except FileNotFoundError:
        alerts = []
    try:
        with open(PAST_ALERTS_PATH) as f:
            past_alerts = json.load(f)
    except FileNotFoundError:
        past_alerts = []

    # Get active rules
    active_rules = [r for r in rules if r.get('is_active')]
    # Get rule names that have triggered alerts
    triggered_rule_names = {a['rule_name'] for a in alerts}
    # Find active rules that have NOT triggered an alert
    not_triggered_rules = [r for r in active_rules if r['rule_name'] not in triggered_rule_names]

    return render(request, 'alert_list.html', {
        'alerts': alerts,
        'not_triggered_rules': not_triggered_rules,
        'past_alerts': past_alerts,
    })

def past_alerts(request):
    try:
        with open(PAST_ALERTS_PATH) as f:
            past_alerts = json.load(f)
    except FileNotFoundError:
        past_alerts = []
    return render(request, 'past_alerts.html', {'alerts': past_alerts})

def clear_alerts(request):
    if request.method == "POST":
        # Read current alerts
        try:
            with open(ALERTS_PATH) as f:
                current_alerts = json.load(f)
        except FileNotFoundError:
            current_alerts = []
        
        # Read existing past alerts
        try:
            with open(PAST_ALERTS_PATH) as f:
                past_alerts = json.load(f)
        except FileNotFoundError:
            past_alerts = []
        
        # Move current alerts to past alerts with cleared status and timestamp
        import datetime
        for alert in current_alerts:
            alert['status'] = 'Cleared'
            alert['cleared_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            past_alerts.append(alert)
        
        # Save updated past alerts
        with open(PAST_ALERTS_PATH, 'w') as f:
            json.dump(past_alerts, f, indent=4)
        
        # Clear current alerts
        with open(ALERTS_PATH, 'w') as f:
            json.dump([], f)
    return redirect('alert_list')

def clear_past_alerts(request):
    if request.method == "POST":
        with open(PAST_ALERTS_PATH, 'w') as f:
            json.dump([], f)
    return redirect('past_alerts')