from django.db import models
from django.contrib.auth.models import User

class Lane(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lanes", null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries", null=True)
    name = models.CharField(max_length=100)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name="entries")
    start_date = models.CharField(max_length=7, blank=True, null=True)
    end_date = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name
    
