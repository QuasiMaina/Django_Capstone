# seed.py
from game.models import Question, Choice

# Clear old data
Question.objects.all().delete()
Choice.objects.all().delete()

# Create sample questions
q1 = Question.objects.create(text="You find yourself at a crowded party. What do you do?")
q2 = Question.objects.create(text="A stranger asks you for help in public. How do you react?")
q3 = Question.objects.create(text="You have a deadline coming up. What’s your coping mechanism?")

# Add choices for each question
Choice.objects.create(question=q1, text="Stay close to someone you know", anxiety_trait="social")
Choice.objects.create(question=q1, text="Find a quiet corner", anxiety_trait="avoidant")
Choice.objects.create(question=q1, text="Mingle with as many people as possible", anxiety_trait="none")

Choice.objects.create(question=q2, text="Freeze and panic", anxiety_trait="general")
Choice.objects.create(question=q2, text="Try to help despite discomfort", anxiety_trait="social")
Choice.objects.create(question=q2, text="Pretend not to hear and walk away", anxiety_trait="avoidant")

Choice.objects.create(question=q3, text="Procrastinate until last minute", anxiety_trait="general")
Choice.objects.create(question=q3, text="Over-plan and obsess", anxiety_trait="ocd")
Choice.objects.create(question=q3, text="Go with the flow, it’ll get done", anxiety_trait="none")

print("✅ Seed data created.")
