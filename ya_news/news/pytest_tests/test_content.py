from http.client import OK

from django.urls import reverse

import pytest

from .common import Routes, NEWS_COUNT_ON_HOME_PAGE, Urls
from news.forms import CommentForm
from news.models import News


@pytest.mark.django_db
def test_news_count(client, list_of_news):
    response = client.get(Routes.URL_HOME)
    assert response.status_code == OK
    if News.objects.count() > NEWS_COUNT_ON_HOME_PAGE:
        news_list = response.context['object_list']
        news_count = news_list.count()
        assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, list_of_news):
    response = client.get(Routes.URL_HOME)
    assert response.status_code == OK
    news_list = list(response.context['object_list'])
    sorted_news = sorted(
        news_list,
        key=lambda news: news.date,
        reverse=True
    )
    assert sorted_news == news_list


@pytest.mark.django_db
def test_comments_order(client, news, list_of_comments):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == OK
    piece_of_news = response.context['news']
    comments_list = list(piece_of_news.comment_set.all())
    sorted_comments = sorted(
        comments_list,
        key=lambda comments: comments.created
    )
    assert sorted_comments == comments_list


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_in_list',
    (
        (Urls.AUTHOR, True),
        (Urls.ANY_USER, False)
    )
)
def test_unauthorized_client_has_no_form(
    parametrized_client,
    form_in_list,
    comment
):
    url = reverse('news:detail', args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == OK
    assert ('form' in response.context) is form_in_list
    if 'form' in response.context:
        assert isinstance(response.context['form'], CommentForm)
