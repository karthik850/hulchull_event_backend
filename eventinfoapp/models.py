from django.db import models

class Events(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Highlights(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return self.name
    