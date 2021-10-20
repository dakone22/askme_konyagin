from django.urls import reverse


# https://dbdiagram.io/d/5e0113e0edf08a25543f5d09

def get_url_func(url: str):
    def get_url(self):
        return reverse(url, args=[str(self.id)])

    return get_url


def get_html_link(self, style="text-info"):
    return f'<a class="{style}" href="{self.url()}">{str(self)}</a>'


from .profile import Profile
from .question import Question, Answer, Tag
from .votes import QuestionVote, AnswerVote
