from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .votes import QuestionVote, AnswerVote
from ..utils import unique_slug_generator


# ======== Tag ========

class TagQuerySet(models.QuerySet):
    def top(self) -> models.QuerySet:
        return self.annotate(count=Count('question')).order_by('-count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark']
    color_id = models.IntegerField(choices=[(index, color_id) for index, color_id in enumerate(colors)])

    objects = TagQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name

    def color(self) -> str:
        return self.colors[self.color_id]

    def questions(self) -> models.QuerySet['Question']:
        return self.question_set.all()

    def question_count(self) -> int:
        return self.question_set.count()


@receiver(pre_save, sender=Tag)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# ======== Question ========

class QuestionQuerySet(models.QuerySet):
    def from_author(self, author: User) -> models.QuerySet:
        return self.filter(author=author)

    def latest(self, from_date: datetime = None) -> models.QuerySet:
        if from_date is None:
            from_date = datetime.now() - timedelta(hours=1)
        return self.filter(date__gte=from_date)

    def popular(self) -> models.QuerySet:
        return self.annotate(num_votes=Count('questionvote', filter=Q(questionvote__type=True)) -
                                       Count('questionvote', filter=Q(questionvote__type=False))) \
            .order_by('-num_votes')


class Question(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    date = models.DateTimeField(verbose_name='Creation date')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)

    tags = models.ManyToManyField(to=Tag)

    objects = QuestionQuerySet.as_manager()

    def __str__(self) -> str:
        return self.title

    def answers(self) -> models.QuerySet:
        return Answer.objects.filter(question=self)

    def correct_answers(self) -> models.QuerySet:
        return self.answers().get(correct=True)

    def votes(self) -> int:
        my_votes = QuestionVote.objects.filter(question=self)
        return my_votes.filter(type=True).count() - my_votes.filter(type=False).count()

    def top_tags(self, limit=5) -> models.QuerySet:
        return self.tags.annotate(count=Count('question')).order_by('-count')[:limit]


# ======== Answer ========

class AnswerQuerySet(models.QuerySet):
    def from_author(self, author: User) -> models.QuerySet:
        return self.filter(author=author)


class Answer(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    date = models.DateTimeField(verbose_name='Creation date')
    text = models.TextField(max_length=1000)
    correct = models.BooleanField(verbose_name="Is Correct", default=False)

    objects = AnswerQuerySet.as_manager()

    def is_correct(self) -> bool:
        return self.correct

    def votes(self) -> int:
        my_votes = AnswerVote.objects.filter(answer=self)
        return my_votes.filter(type=True).count() - my_votes.filter(type=False).count()
