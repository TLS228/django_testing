from datetime import timedelta

import pytest
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.test.client import Client

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def news_list():
    today = timezone.now()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.)',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_user_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def redirect_edit_url(url_user_login, edit_url):
    return f'{url_user_login}?next={edit_url}'


@pytest.fixture
def redirect_delete_url(url_user_login, delete_url):
    return f'{url_user_login}?next={delete_url}'


@pytest.fixture
def more_comments(author, news):
    now = timezone.now()
    for index in range(20):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
