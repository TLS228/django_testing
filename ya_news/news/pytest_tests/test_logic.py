import pytest

from http import HTTPStatus

from django.shortcuts import get_object_or_404
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news_url,
                                            client, form_data):
    comments_before = Comment.objects.count()
    response = client.post(news_url, data=form_data)
    comments_after = Comment.objects.count()
    assert response.status_code == HTTPStatus.FOUND
    assert comments_before == comments_after


def test_user_can_create_comment(not_author_client,
                                 news_url,
                                 form_data):
    comments_before = Comment.objects.count()
    response = not_author_client.post(news_url, data=form_data)
    assertRedirects(response, f'{news_url}#comments')
    comments_after = Comment.objects.count()
    assert comments_after == comments_before + 1


def test_user_cant_use_bad_words(news_url,
                                 not_author_client,
                                 bad_words_fixture):
    response = not_author_client.post(news_url,
                                      data=bad_words_fixture)
    comments_count = Comment.objects.count()
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, delete_url, news_url
):
    comments_before = Comment.objects.count()
    response = author_client.delete(delete_url)
    comments_after = Comment.objects.count()
    assertRedirects(response, f'{news_url}#comments')
    assert comments_after == comments_before - 1


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
        delete_url, admin_client,
):
    comments_before = Comment.objects.count()
    response = admin_client.delete(delete_url)
    comments_after = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments_after == comments_before


def test_author_can_edit_comment(
        author_client, comment, edit_url,
        news_url, form_data
):
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, f'{news_url}#comments')
    comment = get_object_or_404(Comment, pk=comment.pk)
    assert comment.text == 'Новый'


def test_user_cant_edit_comment_of_another_user(
        edit_url, comment, not_author_client, form_data
):
    response = not_author_client.post(edit_url, data=form_data)
    comment = get_object_or_404(Comment, pk=comment.pk)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == 'Текст комментария'
