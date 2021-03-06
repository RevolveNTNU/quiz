from django.db import models


class Tag(models.Model):
    name = models.SlugField(max_length=16, primary_key=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    timestamp = models.DateTimeField(auto_now=True)

    def get_answer_count(self):
        return self.answer_set.aggregate(models.Sum('answered'))['answered__sum']

    def get_wrong_answer_count(self):
        return self.answer_set.filter(correct=False).aggregate(
            models.Sum('answered'))['answered__sum']

    def shuffled_answers(self):
        return self.answer_set.order_by('?')

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    answered = models.IntegerField(default=0)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    def __str__(self):
        return '{}; {}'.format(self.correct, self.text)


class Quiz(models.Model):
    name = models.SlugField(max_length=16, primary_key=True)
    questions = models.ManyToManyField(Question)
