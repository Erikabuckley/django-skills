from datetime import time
from django.contrib.auth import get_user_model
from django.db import models

# room model to record details about the room
class Room(models.Model):
    name = models.CharField(max_length=50)
    floor = models.IntegerField()
    room_number = models.IntegerField()

    def __str__(self):
        return f"{self.name} (room  {self.room_number})"


# meeting table in db has to inherit from the models superclass
class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    duration = models.IntegerField(default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        get_user_model()
    )  # incase db changes we call m2m insted

    def __str__(self):
        return f"{self.title} at {self.start_time} on {self.date}"
