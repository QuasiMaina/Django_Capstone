from rest_framework import serializers
from .models import GameSession, ChoiceLog
from django.contrib.auth.models import User
from .models import Question, Choice


# User Serializer (basic user info)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# GameSession Serializer
class GameSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GameSession
        fields = ['id', 'user', 'session_id', 'created_at', 'current_node', 'scores']


# ChoiceLog Serializer
class ChoiceLogSerializer(serializers.ModelSerializer):
    session = serializers.CharField(source='session.session_id', read_only=True)

    class Meta:
        model = ChoiceLog
        fields = ['id', 'session', 'question', 'choice', 'score_given', 'timestamp']

# Choice serializer for use inside Question
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'score_value', 'next_question']


# Question serializer with nested choices
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'anxiety_type', 'choices']