from django.db import models


class Entry(models.Model):
    title_lower = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=256)

    def __str__(self):
        return f"{self.title}"
