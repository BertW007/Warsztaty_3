from django.db import models


class Room(models.Model):

    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)


class Booking(models.Model):

    date = models.DateField(unique=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)