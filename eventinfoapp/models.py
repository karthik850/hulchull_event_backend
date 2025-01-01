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

    def subtract_points(self, points):
        """Subtracts points from the team's overall points."""
        self.overall_points -= points
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
    def calculate_points_change(self, old_spots, new_spots):
        """Adjust team points based on changes in team spots."""
        point_map = {1: 10, 2: 6, 3: 4, 4: 2, 5: 0}

        for spot, new_team in new_spots.items():
            old_team = old_spots.get(spot)
            if old_team != new_team:  # Only process changes
                if old_team:
                    # Subtract points for the previous position
                    old_team.subtract_points(point_map[spot])
                if new_team:
                    # Add points for the new position
                    new_team.add_points(point_map[spot])

    def save(self, *args, **kwargs):
        """Override save to update team scores only on position changes."""
        if self.pk:
            old_event = Events.objects.get(pk=self.pk)
            old_spots = {
                1: old_event.team_spot_1,
                2: old_event.team_spot_2,
                3: old_event.team_spot_3,
                4: old_event.team_spot_4,
                5: old_event.team_spot_5,
            }
            new_spots = {
                1: self.team_spot_1,
                2: self.team_spot_2,
                3: self.team_spot_3,
                4: self.team_spot_4,
                5: self.team_spot_5,
            }
            self.calculate_points_change(old_spots, new_spots)
        super().save(*args, **kwargs)


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
