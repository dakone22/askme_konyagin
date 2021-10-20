from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpRequest

from .models import Tag, Answer


def sidebar(request: HttpRequest):
    users = User.objects.annotate(count=Count('answer')).order_by('-count')[:10]
    count = [Answer.objects.filter(author=user).count() for user in users]
    extra_context = {
        'top_tags': Tag.objects.top(),
        'top_members': zip(users, count),  # TODO: rework
    }
    return extra_context
