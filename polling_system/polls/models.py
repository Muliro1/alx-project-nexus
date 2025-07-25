from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=40)  # Session/IP hash
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['option', 'voter_id']]  # Prevent duplicate votes
        indexes = [
            models.Index(fields=['voter_id', 'option'])
        ]
