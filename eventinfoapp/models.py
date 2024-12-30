from django.db import models


    

class Teams(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.TextField(help_text="Enter team members' names, separated by commas",null=True, blank=True)
    overall_points = models.IntegerField(default=0)
    image_url = models.URLField(max_length=500,null=True, blank=True)

    def __str__(self):
        return self.name

    def get_members_list(self):
        """Returns the members as a list."""
        return [member.strip() for member in self.members.split(',') if member.strip()]

    def add_points(self, points):
        """Adds points to the team's overall points."""
        self.overall_points += points
        self.save()

    def reset_points(self):
        """Resets the team's overall points to 0."""
        self.overall_points = 0
        self.save()

# class Events(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     location = models.CharField(max_length=300)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    
class Events(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField( null=True, blank=True)
    start_date = models.DateTimeField()
    location = models.CharField(max_length=300)
    team_spot_1 = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='event_team_1', null=True, blank=True)
    team_spot_2 = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='event_team_2', null=True, blank=True)
    team_spot_3 = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='event_team_3', null=True, blank=True)
    team_spot_4 = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='event_team_4', null=True, blank=True)
    team_spot_5 = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='event_team_5', null=True, blank=True)
    image_url=models.URLField(max_length=500,null=True, blank=True)

    def __str__(self):
        return self.name
    def update_team_scores(self):
        """Increase overall score for team in team_spot_1 by 10 points."""
        if self.team_spot_1:
            self.team_spot_1.add_points(10)
        if self.team_spot_2:
            self.team_spot_2.add_points(6)
        if self.team_spot_3:
            self.team_spot_3.add_points(4)
        if self.team_spot_4:
            self.team_spot_4.add_points(2)
        if self.team_spot_5:
            self.team_spot_5.add_points(0)

    def save(self, *args, **kwargs):
        """Override save method to update team scores on save."""
        super().save(*args, **kwargs)
        self.update_team_scores()


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
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',  # Optional: Set a default value
    )

    def __str__(self):
        return self.name
