from django.db import models

class VisualizationModel(models.Model):
    report = models.ForeignKey('ReportModel', on_delete=models.CASCADE)
    visualization_type = models.CharField(max_length=100)
    visualization_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visualization_type} for Report ID: {self.report.id}"