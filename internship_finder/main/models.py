from django.db import models

class Internships(models.Model):

    title = models.CharField()
    company = models.CharField()
    location = models.CharField()
    deadline = models.DateField()
    apply = models.URLField()
