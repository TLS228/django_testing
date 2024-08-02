import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(news_list, home_url, client):
    assert (
        client.get(home_url).context['object_list'].count()
        == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(home_url, client):
    news_list = list(client.get(
        home_url).context['object_list'].values('date'))
    sorted_news_list = sorted(news_list, key=lambda x: x['date'], reverse=True)
    assert news_list == sorted_news_list


def test_comments_order(news_url, client, news, comments):
    response = client.get(news_url)
    assert 'news' in response.context
    news = response.context['news']
    comments = news.comment_set.all()
    created_dates = [comment.created for comment in comments]
    assert created_dates == sorted(created_dates)


def test_form_presence_for_anonymous_client(client, news_url):
    assert 'form' not in client.get(news_url).context


def test_form_presence_for_author_client(author_client, news_url):
    response = author_client.get(news_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
