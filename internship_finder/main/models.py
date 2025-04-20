from django.db import models

class Internships(models.Model):

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    deadline = models.DateField()
    apply = models.URLField(max_length=500)
