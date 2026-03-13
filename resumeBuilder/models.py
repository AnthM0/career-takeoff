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

    # flexible field to store any additional details about the entry, such as dates, descriptions, etc.
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
    ## start_date = models.CharField(max_length=7, blank=True, null=True)
    ## end_date = models.CharField(max_length=7, blank=True, null=True)

    # DETAILS ACCESS FUNCTION
    def get_detail(self, key):
        return self.details.get(key, "")
    
    # DETAILS UPDATE FUNCTION
    def update_detail(self, key, value):
        self.details[key] = value
        self.save()

    # DETAILS DELETE FUNCTION
    def delete_detail(self, key):
        if key in self.details:
            del self.details[key]
            self.save()
