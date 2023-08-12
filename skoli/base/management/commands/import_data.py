import csv
from django.core.management.base import BaseCommand
from base.models import Prov, Quiz, Question, Choise

class Command(BaseCommand):
    help = 'Import questions from CSV file'

    def handle(self, *args, **kwargs):
        csv_file = '/Users/Justus/Desktop/skoli.se/data.csv'  # Replace this with the actual path to your CSV file

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get or create Prov instance
                prov, _ = Prov.objects.get_or_create(title=row['prov_title'])

                # Get the quiz name from the row
                quiz_name = row['quiz_name']

                # Skip the row if the quiz name is empty
                if not quiz_name:
                    self.stdout.write(self.style.WARNING(f"Skipping row with empty quiz name: {row}"))
                    continue

                # Get or create Quiz instance
                quiz, _ = Quiz.objects.get_or_create(prov=prov, name=quiz_name)

                # Get or create Question instance
                question, _ = Question.objects.get_or_create(
                    quiz=quiz,
                    text=row['question_text'],
                    question_count=row['question_count'],
                    img=row['question_img'],
                    question_description_img=row['questiondescription_img'],
                    question_description_txt=row['questiondescription_txt']
                    
                )

                # Get or create Choise instance(s)
                choise_header = row['choise_header']
                choise_text = row['choise_text']
                choise_img = row['choise_img']
                correct_answer = True if row['correct_answer'].lower() == 'true' else False

                choise, _ = Choise.objects.get_or_create(
                    question=question,
                    header=choise_header,
                    text=choise_text,
                    img=choise_img,
                    correct_answer=correct_answer
                )

                # Note: If you have a QuestionDescription model, you can handle it in a similar way.

        self.stdout.write(self.style.SUCCESS('Successfully imported questions'))
