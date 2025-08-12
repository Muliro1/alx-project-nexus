from django.shortcuts import render# Create your views here.
from rest_framework import views, status, generics
from rest_framework.response import Response
from .models import Poll, Option, Vote
from .serializers import PollSerializer, VoteSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from drf_yasg import openapi

def home(request):
    """Home view that displays all available routes"""
    return render(request, 'home.html')

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PollListCreate(generics.ListCreateAPIView):
    queryset = Poll.objects.prefetch_related('options')
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="List all polls (GET) or create a new poll (POST)",
        request_body=PollSerializer,
        responses={
            200: PollSerializer(many=True),
            201: PollSerializer,
            401: openapi.Response(
                description="Authentication credentials were not provided",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="List all polls",
        responses={
            200: PollSerializer(many=True),
            401: openapi.Response(
                description="Authentication credentials were not provided",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    }
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PollResults(views.APIView):
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        options = poll.options.all()
        return Response([{
            'option_id': opt.id,
            'text': opt.text,
            'votes': opt.votes
        } for opt in options])

class VoteCreate(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VoteSerializer,
        operation_description="Vote on a specific option in a poll",
        responses={
            201: openapi.Response(
                description="Vote recorded successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                    }
                )
            ),
            400: openapi.Response(
                description="Validation error or poll expired",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    }
                )
            ),
            404: openapi.Response(
                description="Poll or option not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    }
                )
            ),
        }
    )
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get poll and option with explicit validation
        poll_id = serializer.validated_data['poll_id']
        option_id = serializer.validated_data['option_id']
        
        poll = get_object_or_404(Poll, id=poll_id)
        option = get_object_or_404(Option, id=option_id, poll=poll)
        user = request.user
        
        # Additional validation (redundant but explicit)
        if poll.expires_at < timezone.now():
            return Response({"error": "Poll has expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already voted on this option
        existing_vote = Vote.objects.filter(option=option, voter=user).first()
        if existing_vote:
            return Response({"error": "You have already voted on this option"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create vote
        Vote.objects.create(
            option=option,
            voter=user
        )
        
        # Update vote count
        option.votes = option.votes + 1
        option.save()
        
        return Response({"status": "Vote recorded"}, status=status.HTTP_201_CREATED)

class CustomObtainAuthToken(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Obtain authentication token using username and password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User's username"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User's password"
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Authentication successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description="Authentication token"),
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
                    }
                )
            ),
            400: openapi.Response(
                description="Authentication failed",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

