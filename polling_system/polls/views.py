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
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PollListCreate(generics.ListCreateAPIView):
    queryset = Poll.objects.prefetch_related('options')
    serializer_class = PollSerializer

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

    @swagger_auto_schema(request_body=VoteSerializer)
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        option = get_object_or_404(Option, id=serializer.validated_data['option_id'])
        poll = option.poll
        user = request.user
        
        # Check expiration
        if poll.expires_at < timezone.now():
            return Response({"error": "Poll has expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        # Create vote
        Vote.objects.update_or_create(
            option=option,
            voter_id=serializer.validated_data['voter_id'],
            voter = user,
            defaults={}
        )
        
        # Update vote count
        option.votes = option.votes + 1
        option.save()
        
        return Response({"status": "Vote recorded"}, status=status.HTTP_201_CREATED)

class CustomObtainAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

