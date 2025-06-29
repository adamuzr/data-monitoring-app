import json
import os
import subprocess
import sys
from django.conf import settings
from django.shortcuts import render, redirect

RULES_PATH = os.path.join(settings.BASE_DIR, 'data_monitoring_app', 'rules.json')

def rule_list(request):
    try:
        with open(RULES_PATH) as f:
            rules = json.load(f)
    except FileNotFoundError:
        rules = []
    return render(request, 'rule_list.html', {'rules': rules})

def add_rule(request):
    if request.method == 'POST':
        row_count_str = request.POST.get('row_count', '').strip()
        minutes_str = request.POST.get('minutes', '').strip()
        rule = {
            "rule_name": request.POST['rule_name'],
            "table": request.POST['table'],
            "row_count": int(row_count_str) if row_count_str.isdigit() else 100,
            "threshold": request.POST['threshold'],
            "unique_attribute": request.POST.get('unique_attribute', ''),
            "watch_value": request.POST.get('watch_value', ''),
            "check_modification": 'check_modification' in request.POST,
            "severity": request.POST['severity'],
            "description": request.POST['description'],
            "is_active": 'is_active' in request.POST,
            "attribute": request.POST.get('attribute', ''),
            "minutes": int(minutes_str) if minutes_str.isdigit() else 5,
        }
        
        try:
            with open(RULES_PATH) as f:
                rules = json.load(f)
        except FileNotFoundError:
            rules = []
        rules.append(rule)
        with open(RULES_PATH, 'w') as f:
            json.dump(rules, f, indent=4)

        # --- Run monitor.py automatically after saving the rule ---
        script_path = os.path.join(os.path.dirname(__file__), '..', 'monitor.py')
        subprocess.Popen([sys.executable, script_path])

        return redirect('rule_list')
    return render(request, 'add_rule.html')

def delete_rule(request, rule_name):
    with open(RULES_PATH) as f:
        rules = json.load(f)
    rules = [r for r in rules if r['rule_name'] != rule_name]
    with open(RULES_PATH, 'w') as f:
        json.dump(rules, f, indent=4)
    return redirect('rule_list')

def toggle_rule(request, rule_name):
    if request.method == 'POST':
        with open(RULES_PATH, 'r') as f:
            rules = json.load(f)
        for rule in rules:
            if rule['rule_name'] == rule_name:
                rule['is_active'] = not rule['is_active']
                break
        with open(RULES_PATH, 'w') as f:
            json.dump(rules, f, indent=4)
    return redirect('rule_list')

def edit_rule(request, rule_name):
    with open(RULES_PATH) as f:
        rules = json.load(f)
    rule = next((r for r in rules if r['rule_name'] == rule_name), None)
    if not rule:
        return redirect('rule_list')
    if request.method == 'POST':
        rule['rule_name'] = request.POST['rule_name']
        rule['table'] = request.POST['table']
        row_count_str = request.POST.get('row_count', '').strip()
        rule['row_count'] = int(row_count_str) if row_count_str.isdigit() else 100
        rule['threshold'] = request.POST['threshold']
        rule['unique_attribute'] = request.POST.get('unique_attribute', '')
        rule['watch_value'] = request.POST.get('watch_value', '')
        rule['check_modification'] = 'check_modification' in request.POST
        rule['severity'] = request.POST['severity']
        rule['description'] = request.POST['description']
        rule['is_active'] = 'is_active' in request.POST
        rule['attribute'] = request.POST.get('attribute', '')
        minutes_str = request.POST.get('minutes', '').strip()
        rule['minutes'] = int(minutes_str) if minutes_str.isdigit() else 5
        with open(RULES_PATH, 'w') as f:
            json.dump(rules, f, indent=4)
        
        # --- Run monitor.py automatically after editing the rule ---
        script_path = os.path.join(os.path.dirname(__file__), '..', 'monitor.py')
        subprocess.Popen([sys.executable, script_path])

        return redirect('rule_list')

    return render(request, 'edit_rule.html', {'rule': rule})