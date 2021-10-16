from typing import List

from django.contrib.auth.models import User
from django.db import models

from . import get_url_func, get_html_link
from .tag import TagQuestionRel
from .votes import QuestionVote, AnswerVote


class QuestionQuerySet(models.QuerySet):
    def from_author(self, author: User) -> models.QuerySet:
        return self.filter(author=author)

    # def with_tags(self, tags: List[Tag]) -> models.QuerySet:
    #     tr = TagQuestionRel.objects.filter(question=self)
    #     for tag in tags:
    #         tr = tr.filter(tag=tag)
    #     return tr.annotate(F('tag'))  # TODO: check



class Question(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    date = models.DateTimeField(verbose_name='Creation date')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return self.title

    url = get_url_func('question')
    html = get_html_link

    def tags(self) -> List['Tag']:
        return [tqr.tag for tqr in TagQuestionRel.objects.filter(question=self)]

    def answers(self) -> models.QuerySet:
        return Answer.objects.filter(question=self)

    def correct_answers(self) -> models.QuerySet:
        return self.answers().get(correct=True)

    def votes(self) -> int:
        votes = QuestionVote.objects.filter(question=self)
        return votes.filter(type=True).count() - votes.filter(type=False).count()


class AnswerQuerySet(models.QuerySet):
    def from_author(self, author: User):
        return self.filter(author=author)

    def vote_count(self):
        votes = AnswerVote.objects.filter(question=self)
        return votes.filter(type=True).count() - votes.filter(type=False).count()


class Answer(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    date = models.DateTimeField(verbose_name='Creation date')
    text = models.TextField(max_length=1000)
    correct = models.BooleanField(verbose_name="IsCorrect", default=False)

    objects = AnswerQuerySet.as_manager()

    def is_correct(self):
        return self.correct
