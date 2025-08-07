from django.contrib import admin
from .models import Question, Choice, GameSession, ChoiceLog


class ChoiceInline(admin.TabularInline):
    model = Choice
    fk_name = 'question'  # Specify the correct FK since Choice has two FKs to Question
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question', 'next_question')


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'current_node', 'completed', 'created_at')
    list_filter = ('completed',)


@admin.register(ChoiceLog)
class ChoiceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'choice', 'score_given', 'timestamp')
    list_filter = ('session',)