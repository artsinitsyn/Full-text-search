from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=512)
    authors = models.CharField(max_length=512, blank=True)
    genre = models.CharField(max_length=128, blank=True)
    year = models.IntegerField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
