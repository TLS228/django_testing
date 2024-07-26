import pytest

from django.conf import settings

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


def test_comments_order(news_url, client):
    response = client.get(news_url)
    assert 'news' in response.context
    news = response.context['news']
    comments = news.comment_set.all()
    assert list(comments.values_list('created', flat=True)) == list(
        comments.values_list('created', flat=True).order_by('created'))


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True),
    ),
)
def test_pages_contains_form(parametrized_client, expected_status, news_url):
    response = parametrized_client.get(news_url)
    form_in_context = 'form' in response.context
    assert form_in_context == expected_status
    if form_in_context:
        assert 'form' in response.context
