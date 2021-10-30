import random
import string

from django.core.paginator import Paginator
from django.http import HttpRequest
from django.utils.text import slugify


def get_page_object(request: HttpRequest, objects: list, count_on_list=5, adjacent_pages=2):
    raise Exception("Don't use it")  # TODO: DELETE

    paginator = Paginator(objects, count_on_list)
    n = request.GET.get('page')
    page_obj = paginator.get_page(n)

    if int(n) < 1:
        page_obj.number = 1
    if page_obj.number > paginator.num_pages:
        page_obj.number = paginator.num_pages

    start_page = max(page_obj.number - adjacent_pages, 1)
    if start_page <= 3:
        start_page = 1
    end_page = page_obj.number + adjacent_pages + 1
    if end_page >= paginator.num_pages - 1:
        end_page = paginator.num_pages + 1

    page_numbers = [n for n in range(start_page, end_page) if n in range(1, paginator.num_pages + 1)]

    page_obj.page_numbers = page_numbers
    page_obj.show_first = 1 not in page_numbers
    page_obj.show_last = paginator.num_pages not in page_numbers

    return page_obj


# https://www.geeksforgeeks.org/add-the-slug-field-inside-django-model/

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug[:max_length - 5], randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
