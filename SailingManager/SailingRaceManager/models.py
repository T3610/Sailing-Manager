from django.db import models
from datetime import datetime
# Create your models here.
class Race(models.Model):
    RACE_TYPE_CHOICES = [
        (0, 'Handicap'),
        (1, 'Pursuit'),
    ]

    RaceNumber = models.PositiveIntegerField(unique=True)
    StartTime = models.DateTimeField(blank=True, null=True)
    RaceLength = models.PositiveIntegerField(default=40)
    RaceType = models.IntegerField(choices=RACE_TYPE_CHOICES, default=0)

    def __str__(self):
        return "Race "+str(self.RaceNumber)

class Boat(models.Model):
    """Model definition for Boat."""

    # TODO: Define fields here
    BoatName = models.CharField(max_length=50)
    PyNumber = models.PositiveIntegerField()

    def __str__(self):
        """Unicode representation of Boat."""
        return self.BoatName+" - "+str(self.PyNumber)

class Racer(models.Model):
    Boat = models.ForeignKey(Boat, on_delete=models.CASCADE, related_name="Boat", default=1)
    HelmName = models.CharField(max_length=50)
    CrewName = models.CharField(max_length=50, blank=True, null=True)
    SailNumber = models.CharField(max_length=50)
    

    def __str__(self):
        return "Racer - "+self.HelmName

class RaceEvent(models.Model):
    RACE_STATUS_CHOICES = [
        (0, 'FINISHED'),
        (1, 'RETIRED'),
        (2, 'DID NOT START'),
    ]

    Racer = models.ForeignKey(Racer, on_delete=models.CASCADE, related_name='Racer')
    Race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='Race')
    LapsComplete = models.PositiveIntegerField(default=0)
    FinishTime = models.DateTimeField(blank=True, null=True)
    Status = models.IntegerField(choices=RACE_STATUS_CHOICES, blank=True, null=True)
