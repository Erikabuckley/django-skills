from datetime import time

from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50)
    floor = models.IntegerField()
    room_number = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}: room  {self.room_number} on floor {self.floor}"

#table in db has to inherit from the models superclass
class Meeting(models.Model):
    # fields in the table are attributes set in the class
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    duration = models.IntegerField(default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    #as we only added behavior we dont need to make migration
    def __str__(self):
        return f"{self.title} at {self.start_time} on {self.date}"

