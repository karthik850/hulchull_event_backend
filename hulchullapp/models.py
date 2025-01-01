from django.db import models
from django.contrib.auth.models import User


class SecretCodeDB(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    fav_number = models.IntegerField(unique=True)
    associate_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, null=True, blank=True)  # Allows user_name to be empty
    is_opened = models.BooleanField(default=False)
    opened_on = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',  # Optional: Set a default value
    )
    

    def __str__(self):
        return f"{self.associate_name} - {self.fav_number}"
    

# class UsersDB(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user_name = models.TextField()
#     # other fields like picture, address, etc.

#     def __str__(self):
#         return f'{self.user.username}-{self.user_name} Profile'
    

