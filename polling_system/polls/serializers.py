from rest_framework import serializers
from .models import Poll, Option, Vote
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
    
    def validate_username(self, value):
        # Check for username complexity
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        return value
    
    def validate_password(self, value):
        # Check password strength
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']
    
    def validate_text(self, value):
        # Sanitize and validate option text
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Option text cannot be empty.")
        if len(value) > 100:
            raise serializers.ValidationError("Option text cannot exceed 100 characters.")
        # Remove potentially dangerous characters
        value = re.sub(r'[<>"\']', '', value)
        return value.strip()

class PollSerializer(WritableNestedModelSerializer):
    options = OptionSerializer(many=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']
    
    def validate_question(self, value):
        # Sanitize and validate question
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Question must be at least 5 characters long.")
        if len(value) > 200:
            raise serializers.ValidationError("Question cannot exceed 200 characters.")
        # Remove potentially dangerous characters
        value = re.sub(r'[<>"\']', '', value)
        return value.strip()
    
    def validate_expires_at(self, value):
        # Ensure poll doesn't expire in the past
        if value <= timezone.now():
            raise serializers.ValidationError("Poll expiration must be in the future.")
        # Ensure poll doesn't expire too far in the future (max 1 year)
        if value > timezone.now() + timedelta(days=365):
            raise serializers.ValidationError("Poll cannot expire more than 1 year from now.")
        return value
    
    def validate_options(self, value):
        # Ensure poll has at least 2 options
        if len(value) < 2:
            raise serializers.ValidationError("Poll must have at least 2 options.")
        if len(value) > 10:
            raise serializers.ValidationError("Poll cannot have more than 10 options.")
        
        # Ensure option texts are unique
        texts = [option.get('text', '').strip().lower() for option in value]
        if len(texts) != len(set(texts)):
            raise serializers.ValidationError("All options must be unique.")
        
        return value

class VoteSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    voter_id = serializers.CharField(max_length=40, required=False)
    
    def validate_option_id(self, value):
        # Ensure option exists and poll hasn't expired
        try:
            option = Option.objects.get(id=value)
            if option.poll.expires_at < timezone.now():
                raise serializers.ValidationError("Cannot vote on expired poll.")
        except Option.DoesNotExist:
            raise serializers.ValidationError("Invalid option ID.")
        return value
