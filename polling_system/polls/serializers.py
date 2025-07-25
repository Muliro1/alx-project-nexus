from rest_framework import serializers
from .models import Poll, Option, Vote
from drf_writable_nested import WritableNestedModelSerializer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class PollSerializer(WritableNestedModelSerializer):
    options = OptionSerializer(many=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']


class VoteSerializer(serializers.Serializer):
    class Meta:
        model = Vote
        fields = ['option_id', 'voter_id']
        
    option_id = serializers.IntegerField()
    voter_id = serializers.CharField(max_length=40)
