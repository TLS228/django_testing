from datetime import datetime, timedelta

import pytest  # type: ignore
from django.conf import settings  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.test import Client  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore

from news.models import Comment, News

User = get_user_model()


TEXT_COMMENT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Новый текст комментария'


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости'
    )


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.)',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_url(pk_news):
    newse = reverse('news:detail', args=(pk_news))
    return newse


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def public_urls(home_url, detail_url, login_url):
    return (
        home_url,
        detail_url,
        login_url,
        reverse('users:logout'),
        reverse('users:signup'),
    )


@pytest.fixture
def private_urls(edit_url, delete_url):
    return (edit_url, delete_url)


@pytest.fixture
def author():
    return User.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader():
    return User.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text=TEXT_COMMENT
    )


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)


@pytest.fixture
def url_to_comments(detail_url):
    return f'{detail_url}#comments'
