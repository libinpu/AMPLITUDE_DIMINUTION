from django.db import models

class Document(models.Model):
    content = models.TextField()
    exit = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='documents/')
