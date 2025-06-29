from django.db import models

class RuleModel(models.Model):
    SEVERITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    rule_name = models.CharField(max_length=100, unique=True)
    table = models.CharField(max_length=100)
    attribute = models.CharField(max_length=100)
    row_count = models.IntegerField()
    threshold = models.CharField(max_length=2, choices=[('<', '<'), ('>', '>'), ('=', '=')])
    unique_attribute = models.CharField(max_length=100, blank=True, null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Medium')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.rule_name

    class Meta:
        verbose_name = "Rule"
        verbose_name_plural = "Rules"