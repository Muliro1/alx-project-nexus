from rest_framework import serializers
from .models import Poll, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']

class VoteSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    voter_id = serializers.CharField(max_length=40)
