import json
from django.core.management.base import BaseCommand
from game.models import Question, Choice

class Command(BaseCommand):
    help = 'Load initial questions and choices from JSON file'

    def handle(self, *args, **kwargs):
        # Update the path to the JSON file
        json_file_path = 'game/fixtures/initial_questions.json'
        
        try:
            with open(json_file_path) as f:
                data = json.load(f)
                for item in data:
                    if item['model'] == 'game.question':
                        question = Question.objects.create(text=item['fields']['text'])
                    elif item['model'] == 'game.choice':
                        Choice.objects.create(
                            question=question,
                            text=item['fields']['text'],
                            disorder_type=item['fields'].get('disorder_type'),
                            score=item['fields']['score'],
                            next_question=Question.objects.get(pk=item['fields']['next_question']) if item['fields']['next_question'] else None
                        )
            self.stdout.write(self.style.SUCCESS('Successfully loaded initial questions and choices'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('JSON file not found. Please check the path.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON. Please check the file format.'))
