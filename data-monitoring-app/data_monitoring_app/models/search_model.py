from django.db import models

class SearchModel(models.Model):
    query = models.CharField(max_length=255)
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

    class Meta:
        verbose_name = "Search Query"
        verbose_name_plural = "Search Queries"