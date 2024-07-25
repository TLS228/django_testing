from datetime import datetime, timedelta

from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

import pytest

from .common import Routes, NEWS_COUNT_ON_HOME_PAGE
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор',)


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель',)


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def list_of_news():
    now = datetime.today()
    all_news = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость {index}.',
            text=f'Текст новости {index}.'
        )
        news.date = now - timedelta(days=index)
        all_news.append(news)
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text='Текст',
        news=news,
        author=author,
    )
    return comment


@pytest.fixture
def post_comment():
    return {'text': 'Комментарий'}


@pytest.fixture
def list_of_comments(news, author):
    now = timezone.now()
    comments = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Комментарий {index}.'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)
    return comments


@pytest.fixture
def home_url():
    return Routes.URL_HOME


@pytest.fixture
def login_url():
    return Routes.LOGIN_URL


@pytest.fixture
def logout_url():
    return Routes.URL_LOGOUT


@pytest.fixture
def signup_url():
    return Routes.URL_SIGNUP


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))
