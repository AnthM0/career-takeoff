from django.db import models

class Lane(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Entry(models.Model):
    name = models.CharField(max_length=100)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name="entries")
    start_date = models.CharField(max_length=7, blank=True, null=True)
    end_date = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name
    
