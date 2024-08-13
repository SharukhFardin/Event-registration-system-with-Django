from django.db import models
from accountio.models import User

from sharedio.models import BaseModelWithUID


class Event(BaseModelWithUID):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    available_slots = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
