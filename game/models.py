from django.db import models
from django.contrib.auth.models import User



class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  # Show first 50 chars


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices_for_question'
    )
    text = models.CharField(max_length=255)
    next_question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='choices_that_point_here'
    )

    def __str__(self):
        return f"{self.text} (from Q{self.question.id})"

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    current_node = models.ForeignKey('Question', null=True, blank=True, on_delete=models.SET_NULL)
    scores = models.JSONField(default=dict)  

    completed = models.BooleanField(default=False)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session {self.id} for {self.user.username}"


class ChoiceLog(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    score_given = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q{self.question.id} → {self.choice.text}"
    

