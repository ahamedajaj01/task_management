from django.db import models

# Create your models here.
class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        IN_PROGRESS = 'InProgress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'

    class Priority(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=100, choices=Priority.choices, default=Priority.LOW)

    def __str__(self):
        return self.title

