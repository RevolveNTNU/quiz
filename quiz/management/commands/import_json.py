import json

from django.core.management import BaseCommand
from django.db import transaction

from quiz.models import Question, Tag, Answer


class Command(BaseCommand):
    help = 'Import old quiz json data.'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        with open(options['file'], 'r', encoding='utf-8-sig') as file, transaction.atomic():
            imported_tag, _ = Tag.objects.get_or_create(name='importert')
            for quiz in json.load(file):
                quiz_tag, _ = Tag.objects.get_or_create(name=quiz['id'])
                for task in quiz['questions']:
                    question = Question.objects.create(text=task['question'])
                    question.tags.add(imported_tag, quiz_tag)
                    for i, answer in enumerate(task['answers']):
                        Answer.objects.create(text=answer, question=question, correct=(i == 0))
