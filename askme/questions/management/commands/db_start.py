import os
import random
import string
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from questions.models import QuestionVote, AnswerVote
from questions.models import Tag, Question, Answer
from questions.models.tag import TagQuestionRel


def _get_str(chars, rang):
    return ''.join([random.choice(chars) for _ in range(random.randint(*rang))])


def get_username():
    return _get_str(string.ascii_letters, (5, 25))


def get_email():
    return _get_str(string.ascii_letters + string.digits, (5, 25)) + "@" + \
           _get_str(string.ascii_lowercase, (5, 25)) + "." + _get_str(string.ascii_lowercase, (2, 4))


def get_password():
    return _get_str(string.printable, (5, 50))


try:
    import markovify

    with open(os.path.join(__file__, '..', 'data.txt')) as f:
        text = f.read()
    text_model = markovify.Text(text)
    get_title = lambda: text_model.make_short_sentence(100, 10)


    def get_text():
        while True:
            text = text_model.make_short_sentence(750, 300)
            if text: return text
except ImportError:
    get_title = get_username


    def get_text():
        return _get_str(string.ascii_letters + ' ' * 20, (750, 300))


class Command(BaseCommand):
    help = 'Generate start up DB'

    def handle(self, *args, **options):
        print("Creating users...")
        for _ in range(15):
            u = User.objects.create_user(username=get_username(), email=get_email(), password=get_password())
            print(f"New user {u}")
            u.save()

        print("Creating tags...")
        for _ in range(15):
            t = Tag.objects.create(name=f"Tag{_}", color=random.randint(0, 5))
            print(f"New tag {t}")
            t.save()

        print("Creating questions...")
        for _ in range(10):
            q = Question.objects.create(
                author=random.choice(User.objects.all()),
                date=datetime.now(),
                title=get_title(),
                text=get_text(),
            )
            print(f"New question {q}")
            q.save()

            print("linking tags...")
            for _ in range(random.randint(1, 10)):
                while True:
                    print(f"tag {_}")
                    tag = random.choice(Tag.objects.all())
                    if not TagQuestionRel.objects.filter(tag=tag, question=q):
                        tqr = TagQuestionRel.objects.create(tag=tag, question=q)
                        print(f"new tag link {tqr}")
                        tqr.save()
                        break

            print("creating answers...")
            for _ in range(random.randint(1, 15)):
                a = Answer.objects.create(
                    author=random.choice(User.objects.all()),
                    question=q,
                    date=datetime.now(),
                    text=get_text(),
                )
                print(f"new answers {a}")
                a.save()

        print("Creating votes")
        for _ in range(100):
            v = QuestionVote.objects.create(
                user=random.choice(User.objects.all()),
                question=random.choice(Question.objects.all()),
                type=random.randint(0, 100) > 20,
            )
            print(f"created {v}")
            v.save()
        for _ in range(200):
            v = AnswerVote.objects.create(
                user=random.choice(User.objects.all()),
                answer=random.choice(Answer.objects.all()),
                type=random.randint(0, 100) > 20,
            )
            print(f"created {v}")
            v.save()
