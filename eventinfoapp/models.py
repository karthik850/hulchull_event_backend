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
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500,null=True, blank=True)
    ender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',  # Optional: Set a default value
    )

    def __str__(self):
        return self.name
    
class ImportantPersons(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500,null=True, blank=True)
    ender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',  # Optional: Set a default value
    )

    def __str__(self):
        return self.name