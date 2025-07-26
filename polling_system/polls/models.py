from django.db import models
from django.contrib.auth import get_user_model

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
    voter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['option', 'voter']]  # Prevent duplicate votes
        indexes = [
            models.Index(fields=['voter', 'option'])
        ]
