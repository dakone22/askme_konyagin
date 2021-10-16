from typing import List

from django.db import models
from django.db.models import Count

from . import get_url_func


class TagQuerySet(models.QuerySet):
    def top(self):
        return self.annotate(num_questions=Count('Question__id')).order_by('-num_questions')[:10]


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

    def questions(self) -> List['Question']:
        return [tqr.tag for tqr in TagQuestionRel.objects.filter(tag=self)]

    def question_count(self):
        return TagQuestionRel.objects.count(tag=self)


class TagQuestionRel(models.Model):
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    question = models.ForeignKey(to='questions.Question', on_delete=models.CASCADE)
