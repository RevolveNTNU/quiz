from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    def __str__(self):
        return '{}; {}'.format(self.correct, self.text)
