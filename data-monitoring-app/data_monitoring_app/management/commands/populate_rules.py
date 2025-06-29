from django.core.management.base import BaseCommand
from ...models.rule_model import RuleModel

class Command(BaseCommand):
    help = 'Populate immutable security monitoring rules'

    def handle(self, *args, **kwargs):
        rules = [
            {
                'rule_name': 'Data Integrity Violation',
                'rule_type': 'INTEGRITY',
                'rule_criteria': 'Detects nulls or invalid references in critical columns',
            },
            {
                'rule_name': 'Unusual Data Pattern',
                'rule_type': 'PATTERN',
                'rule_criteria': 'Detects outliers or unexpected value distributions',
            },
            {
                'rule_name': 'Data Modification Pattern',
                'rule_type': 'MODIFICATION',
                'rule_criteria': 'Detects unauthorized or bulk changes to data',
            },
            {
                'rule_name': 'Data Volume Anomaly',
                'rule_type': 'VOLUME',
                'rule_criteria': 'Detects sudden spikes or drops in row counts',
            },
            {
                'rule_name': 'Aggregate Threshold Breach',
                'rule_type': 'AGGREGATE',
                'rule_criteria': 'Detects SUM, AVG, MAX, MIN exceeding safe thresholds',
            },
        ]
        for rule in rules:
            RuleModel.objects.get_or_create(
                rule_name=rule['rule_name'],
                defaults={**rule, 'is_system_rule': True}
            )
        self.stdout.write(self.style.SUCCESS('Predefined rules populated.'))