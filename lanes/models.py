from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    lane = models.IntegerField()
    start_date = models.CharField(max_length=7, blank=True, null=True)
    end_date = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name