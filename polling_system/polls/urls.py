from django.urls import path
from .views import PollListCreate, PollResults, VoteCreate, UserRegistrationView

urlpatterns = [
    path('', PollListCreate.as_view(), name='poll-list'),
    path('<int:pk>/results/', PollResults.as_view(), name='poll-results'),
    path('vote/', VoteCreate.as_view(), name='cast-vote'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]
