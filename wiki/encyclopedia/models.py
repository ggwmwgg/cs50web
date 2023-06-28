from django.db import models


class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=64, unique=True)
    content = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
