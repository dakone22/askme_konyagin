import random
import string
import urllib.request
import warnings
from argparse import ArgumentParser

import markovify
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import models
from django.utils import timezone  # TODO: random datetime

from questions.models import QuestionVote, AnswerVote
from questions.models import Tag, Question, Answer


def benchmark(func):
    def new_func(*args, **kwargs):
        import time
        import cProfile, pstats, io
        import tracemalloc
        from pstats import SortKey

        start_time = time.time()

        pr = cProfile.Profile()
        pr.enable()
        tracemalloc.start()

        result = func(*args, **kwargs)

        end_time = time.time()
        snapshot = tracemalloc.take_snapshot()
        pr.disable()

        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        top_stats = snapshot.statistics('lineno')
        print("[ Top 10 ]")
        for stat in top_stats[:10]:
            print(stat)

        print(f'Done in {end_time - start_time:.2f} seconds')

        return result

    return new_func


class Faker:
    TEXT_DATA_URL = r'https://raw.githubusercontent.com/brunoklein99/deep-learning-notes/master/shakespeare.txt'
    USERNAMES_URL = r'https://github.com/jeanphorn/wordlist/raw/master/usernames.txt'
    DOMAINS_URL = r'https://raw.githubusercontent.com/fgont/domain-list/master/alexa-domains.txt'
    LANGUAGES_URL = r'https://raw.githubusercontent.com/csurfer/gitlang/master/languages.txt'
    WORDS_URL = r'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'

    def __init__(self):
        self.text_model = markovify.Text('\n'.join(self._load_lines(Faker.TEXT_DATA_URL)))
        self.username_list = self._load_lines(Faker.USERNAMES_URL)
        self.domain_list = ['google.com']  # self._load_lines(Faker.DOMAINS_URL)
        self.words_list = self._load_lines(Faker.WORDS_URL) + self._load_lines(Faker.LANGUAGES_URL)

    @staticmethod
    def _load_lines(url: str, encoding='utf-8') -> list[str]:
        print(f'Downloading {url}...')
        file = urllib.request.urlopen(url)

        result = []
        for line in file:
            try:
                decoded_line = line.decode(encoding)
            except UnicodeDecodeError:
                print(line, repr(line))
            else:
                result.append(decoded_line.strip())

        return result

    def username(self):
        return random.choice(self.username_list)

    def domain(self):
        return random.choice(self.domain_list)

    def email(self):
        return self.username() + '@' + self.domain()

    @staticmethod
    def _safe_markov(get: callable):
        while True:
            if text := get():
                return text
            warnings.warn("Markov return a null!")

    def title(self):
        return self._safe_markov(lambda: self.text_model.make_short_sentence(100, 10))

    def text(self):
        return self._safe_markov(lambda: self.text_model.make_short_sentence(750, 300))

    def tag(self):
        return random.choice(self.words_list)

    @staticmethod
    def chars(charset: str, min: int, max: int):
        return ''.join([random.choice(charset) for _ in range(random.randint(min, max))])

    @staticmethod
    def password():
        return Faker.chars(string.printable, 5, 50)

    @staticmethod
    def datetime(start: timezone.datetime, end: timezone.datetime = None):
        end = end or timezone.now()
        assert start < end
        delta = timezone.timedelta(seconds=random.randint(1, round((end - start).total_seconds())))
        return start + delta


class Filler:
    def __init__(self,
                 faker: Faker,
                 users: int,
                 tags: int,
                 questions: int,
                 tags_per_question: int,
                 answers: int,
                 question_votes: int,
                 answer_votes: int,
                 ):
        self.faker = faker
        self.users = users
        self.tags = tags
        self.questions = questions
        self.tags_per_question = tags_per_question
        self.answers = answers
        self.question_votes = question_votes
        self.answer_votes = answer_votes

    @staticmethod
    def _fill(model: type[models.Model], count: int, create: callable, after: callable = None):
        cur = model.objects.count()
        print(f"Filling {model} [{cur}/{count}]...")
        for i in range(count - cur):
            obj = create(i)
            print(f'({i}) New {obj}')
            obj.save()

            if after is not None:
                after(obj)
        print()

    @staticmethod
    def get_start_date():
        return timezone.now() - timezone.timedelta(days=7)

    @property
    def start_date(self):
        return self.get_start_date()

    @benchmark
    def fill(self):
        self.fill_users()
        self.fill_tags()

        self.fill_questions()

        self.fill_answers()
        self.fill_votes()

    def fill_users(self):
        self._fill(
            model=User,
            count=self.users,
            create=lambda i: User.objects.create_user(username=self.faker.username(),
                                                      email=self.faker.email(),
                                                      password=self.faker.password())
        )

    def fill_tags(self):
        self._fill(
            model=Tag,
            count=self.tags,
            create=lambda i: Tag.objects.create(name=self.faker.tag(), color_id=random.randint(0, 5))
        )

    def fill_questions(self):
        def after(q: Question):
            tag_count = random.randint(1, self.tags_per_question)
            # tags = random.sample(Tag.objects.all(), tag_count)  # TODO: check memory usage !!!
            tags = [random.choice(Tag.objects.all()) for _ in range(tag_count)]
            print(f"Adding tags: {tags}")
            for tag in tags:
                q.tags.add(tag)

        self._fill(
            model=Question,
            count=self.questions,
            create=lambda i: Question.objects.create(
                author=random.choice(User.objects.all()),  # TODO: check memory usage
                date=self.faker.datetime(self.start_date),
                title=self.faker.title(),
                text=self.faker.text(),
            ),
            after=after,
        )

    def fill_answers(self):
        self._fill(
            model=Answer,
            count=self.answers,
            create=lambda i: Answer.objects.create(
                author=random.choice(User.objects.all()),  # TODO: check memory usage
                question=random.choice(Question.objects.all()),  # TODO: check memory usage
                date=self.faker.datetime(self.start_date),
                text=self.faker.text(),
            )
        )

    def fill_votes(self):
        self._fill(
            model=QuestionVote,
            count=self.question_votes,
            create=lambda i: QuestionVote.objects.create(
                user=random.choice(User.objects.all()),  # TODO: check memory usage
                question=random.choice(Question.objects.all()),  # TODO: check memory usage
                type=random.randint(0, 100) > 10,
            )
        )

        self._fill(
            model=AnswerVote,
            count=self.answer_votes,
            create=lambda i: AnswerVote.objects.create(
                user=random.choice(User.objects.all()),  # TODO: check memory usage
                answer=random.choice(Answer.objects.all()),  # TODO: check memory usage
                type=random.randint(0, 100) > 20,
            )
        )


class Command(BaseCommand):
    help = 'Fill DB with random data'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            '--big',
            help='A looot of data',
            action='store_true',
        )

    def handle(self, *args, **options):
        quantities = {
            'users': 10_000,
            'tags': 10_000,
            'questions': 100_000,
            'tags_per_question': 15,
            'answers': 1_000_000,
            'question_votes': 1_000_000,
            'answer_votes': 1_000_000,
        } if options['big'] else {
            'users': 30,
            'tags': 30,
            'questions': 30,
            'tags_per_question': 10,
            'answers': 15,
            'question_votes': 100,
            'answer_votes': 200,
        }

        print("Initing faker...")
        faker = Faker()

        print("Filling DB with:")
        print('\n'.join([f"{key} = {value}" for key, value in quantities.items()]))

        filler = Filler(faker, **quantities)

        filler.fill()
