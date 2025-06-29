from django.db import models

class ReportModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
    rules_applied = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"