import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db


def test_news_count(news_list, home_url, client):
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(home_url, client):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(news_url, client):
    response = client.get(news_url)
    news = response.context['news']
    comments = news.comment_set.all()
    dates = [comment.created for comment in comments]
    dates_sorted = sorted(dates)
    assert 'news' in response.context
    assert dates == dates_sorted


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True),
    ),
)
def test_pages_contains_form(parametrized_client, expected_status,
                             news_url):
    response = parametrized_client.get(news_url)
    assert ('form' in response.context) is expected_status
