from rest_framework import serializers
from .models import Question, Choice

class NextQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']

class ChoiceSerializer(serializers.ModelSerializer):
    next_question = NextQuestionSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'text', 'disorder_type', 'score', 'next_question']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']
