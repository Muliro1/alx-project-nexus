import graphene
from graphene_django import DjangoObjectType
from .models import Poll, Option, Vote
from django.contrib.auth import get_user_model

class PollType(DjangoObjectType):
    class Meta:
        model = Poll
        fields = ("id", "question", "created_at", "expires_at", "options")

class OptionType(DjangoObjectType):
    class Meta:
        model = Option
        fields = ("id", "poll", "text", "votes")

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = ("id", "option", "voter", "voted_at")

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")

class Query(graphene.ObjectType):
    all_polls = graphene.List(PollType)
    all_options = graphene.List(OptionType)
    all_votes = graphene.List(VoteType)
    all_users = graphene.List(UserType)

    def resolve_all_polls(root, info):
        return Poll.objects.all()

    def resolve_all_options(root, info):
        return Option.objects.all()

    def resolve_all_votes(root, info):
        return Vote.objects.all()

    def resolve_all_users(root, info):
        return get_user_model().objects.all()

schema = graphene.Schema(query=Query)
