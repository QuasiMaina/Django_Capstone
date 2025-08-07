from django.core.management.base import BaseCommand
from game.models import Question, Choice


class Command(BaseCommand):
    help = "Seed the database with questions and choices tied to anxiety types"

    def handle(self, *args, **kwargs):
        # Clear previous data
        Choice.objects.all().delete()
        Question.objects.all().delete()

        # Questions
        q1 = Question.objects.create(text="How often do you avoid eye contact or speaking in public?")
        q2 = Question.objects.create(text="Do you frequently feel tense or worried about the future?")
        q3 = Question.objects.create(text="Have you ever had a sudden surge of intense fear or discomfort?")
        q4 = Question.objects.create(text="Do you find yourself overthinking conversations after they happen?")
        q5 = Question.objects.create(text="Do you experience chest tightness or racing heart in stressful moments?")
        q6 = Question.objects.create(text="You’ve completed the test. Ready for your result.")

        # Choices (linked with anxiety types)
        Choice.objects.create(question=q1, text="Always", next_question=q2, anxiety_type='social')
        Choice.objects.create(question=q1, text="Sometimes", next_question=q2, anxiety_type='none')
        Choice.objects.create(question=q1, text="Never", next_question=q2, anxiety_type='none')

        Choice.objects.create(question=q2, text="Yes, daily", next_question=q3, anxiety_type='gad')
        Choice.objects.create(question=q2, text="Only when things go wrong", next_question=q3, anxiety_type='none')
        Choice.objects.create(question=q2, text="Not really", next_question=q3, anxiety_type='none')

        Choice.objects.create(question=q3, text="Yes, multiple times", next_question=q4, anxiety_type='panic')
        Choice.objects.create(question=q3, text="Once or twice", next_question=q4, anxiety_type='panic')
        Choice.objects.create(question=q3, text="Never", next_question=q4, anxiety_type='none')

        Choice.objects.create(question=q4, text="All the time", next_question=q5, anxiety_type='social')
        Choice.objects.create(question=q4, text="Sometimes", next_question=q5, anxiety_type='none')
        Choice.objects.create(question=q4, text="No", next_question=q5, anxiety_type='none')

        Choice.objects.create(question=q5, text="Frequently", next_question=q6, anxiety_type='panic')
        Choice.objects.create(question=q5, text="Occasionally", next_question=q6, anxiety_type='gad')
        Choice.objects.create(question=q5, text="Not really", next_question=q6, anxiety_type='none')

        Choice.objects.create(question=q6, text="Show me my result", next_question=None, anxiety_type='none')

        self.stdout.write(self.style.SUCCESS("✅ Seeded questions and anxiety-linked choices."))
