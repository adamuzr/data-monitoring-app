from django.db import models
from .rule_model import RuleModel

class AlertModel(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Resolved', 'Resolved'),
    ]
    alert_name = models.CharField(max_length=150)
    rule = models.ForeignKey(RuleModel, on_delete=models.CASCADE)
    table = models.CharField(max_length=100)
    attribute = models.CharField(max_length=100)
    row_count = models.IntegerField()
    threshold = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10)
    details = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.alert_name} ({self.created_at})"

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"