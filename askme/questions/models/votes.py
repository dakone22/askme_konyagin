from django.contrib.auth.models import User
from django.db import models

vote_type = (
    (False, 'Down'),
    (True, 'Up'),
)


class QuestionVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to='questions.Question', on_delete=models.CASCADE)
    type = models.BooleanField(choices=vote_type)


class AnswerVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    answer = models.ForeignKey(to='questions.Answer', on_delete=models.CASCADE)
    type = models.BooleanField(choices=vote_type)
