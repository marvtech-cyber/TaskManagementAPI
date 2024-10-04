from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    PRIORITY_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]

    STATUS = [

        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority_level = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=10, choices=STATUS)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
