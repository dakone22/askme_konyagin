from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

from . import get_url_func, get_html_link
from .votes import QuestionVote, AnswerVote


class TagQuerySet(models.QuerySet):
    def top(self):
        return self.annotate(num_questions=Count('question__id')).order_by('-num_questions')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark']
    color = models.IntegerField(choices=[(index, color) for index, color in enumerate(colors)])

    objects = TagQuerySet.as_manager()

    def __str__(self):
        return self.name

    url = get_url_func('tag')

    def html(self):
        return f'<a href="{self.url()}"><span class="badge rounded-pill bg-{self.colors[self.color]}">{str(self)}</span></a>'

    def questions(self) -> models.QuerySet['Question']:
        return self.question_set.all()

    def question_count(self) -> int:
        return self.question_set.count()


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

    tags = models.ManyToManyField(to=Tag)

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return self.title

    url = get_url_func('question')
    html = get_html_link

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
    correct = models.BooleanField(verbose_name="Is Correct", default=False)

    objects = AnswerQuerySet.as_manager()

    def is_correct(self):
        return self.correct
