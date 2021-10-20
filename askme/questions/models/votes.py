from django.contrib.auth.models import User
from django.db import models

vote_type = (
    (False, 'Down'),
    (True, 'Up'),
)


class QuestionVoteQuerySet(models.QuerySet):
    def from_question(self, question):
        return self.filter(question=question)


class QuestionVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to='questions.Question', on_delete=models.CASCADE)
    type = models.BooleanField(choices=vote_type)

    objects = QuestionVoteQuerySet.as_manager()


class AnswerVoteQuerySet(models.QuerySet):
    def from_question(self, answer):
        return self.filter(answer=answer)


class AnswerVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    answer = models.ForeignKey(to='questions.Answer', on_delete=models.CASCADE)
    type = models.BooleanField(choices=vote_type)

    objects = AnswerVoteQuerySet.as_manager()
