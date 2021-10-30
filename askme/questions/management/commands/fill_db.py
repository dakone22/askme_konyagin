import os
import random
import string

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils import timezone  # TODO: random datetime

from questions.models import QuestionVote, AnswerVote
from questions.models import Tag, Question, Answer


def _get_str(chars, rang):
    return ''.join([random.choice(chars) for _ in range(random.randint(*rang))])


def get_username():  # TODO: random usernames
    return _get_str(string.ascii_letters, (5, 15))


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

    def get_title():
        return text_model.make_short_sentence(100, 10)


    def get_text():
        while True:
            text = text_model.make_short_sentence(750, 300)
            if text: return text
except ImportError:
    get_title = get_username


    def get_text():
        return _get_str(string.ascii_letters + ' ' * 20, (750, 300))

COUNTS = {
    'users': 30,
    'tags': 30,
    'questions': 30,
    'tags_link': 10,
    'answers': 15,
    'QuestionVote': 100,
    'AnswerVote': 200,
}


# COUNTS = {
#     'users': 10_000,
#     'tags': 10_000,
#     'questions': 100_000,
#     'tags_link': 15,
#     'answers': 1_000_000,
#     'QuestionVote': 1_000_000,
#     'AnswerVote': 1_000_000,
# }


class Command(BaseCommand):
    help = 'Generate start up DB'

    def handle(self, *args, **options):
        print("Creating users...")
        for _ in range(COUNTS['users']):
            u = User.objects.create_user(username=get_username(), email=get_email(), password=get_password())
            print(f"New user {u}")
            u.save()

        print("Creating tags...")
        for _ in range(COUNTS['users']):
            t = Tag.objects.create(name=f"Tag{_}", color_id=random.randint(0, 5))
            print(f"New tag {t}")
            t.save()

        print("Creating questions...")
        for _ in range(COUNTS['questions']):
            q = Question.objects.create(
                author=random.choice(User.objects.all()),
                date=timezone.now(),
                title=get_title(),
                text=get_text(),
            )
            print(f"New question {q}")
            q.save()

            print("linking tags...")
            for _ in range(random.randint(1, COUNTS['tags_link'])):
                while True:
                    print(f"tag {_}")
                    tag = random.choice(Tag.objects.all())
                    if q not in tag.questions():
                        q.tags.add(tag)
                        print(f"new tag link {q} to {tag}")
                        break

            print("creating answers...")
            for _ in range(random.randint(1, COUNTS['answers'])):
                a = Answer.objects.create(
                    author=random.choice(User.objects.all()),
                    question=q,
                    date=timezone.now(),
                    text=get_text(),
                )
                print(f"new answer {a}")
                a.save()

        print("Creating votes")
        for _ in range(COUNTS['QuestionVote']):
            v = QuestionVote.objects.create(
                user=random.choice(User.objects.all()),
                question=random.choice(Question.objects.all()),
                type=random.randint(0, 100) > 40,
            )
            print(f"created {v}")
            v.save()
        for _ in range(COUNTS['AnswerVote']):
            v = AnswerVote.objects.create(
                user=random.choice(User.objects.all()),
                answer=random.choice(Answer.objects.all()),
                type=random.randint(0, 100) > 40,
            )
            print(f"created {v}")
            v.save()
