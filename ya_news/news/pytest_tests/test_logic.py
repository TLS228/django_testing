import pytest
from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

BAD_WORDS_FIXTURE = {'text': f'Текст раз, {BAD_WORDS[0]}, и дальше'}
FORM_DATA = {'text': 'Новый'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news_url,
                                            client):
    comments_before = list(Comment.objects.values_list('id', flat=True))
    response = client.post(news_url, data=FORM_DATA)
    comments_after = list(Comment.objects.values_list('id', flat=True))
    assert response.status_code == HTTPStatus.FOUND
    assert comments_before == comments_after


def test_user_can_create_comment(not_author_client, news_url,
                                 not_author):
    comments_before = list(Comment.objects.all())
    response = not_author_client.post(news_url, data=FORM_DATA)
    comments_after = list(Comment.objects.all())
    assertRedirects(response, f'{news_url}#comments')
    assert len(comments_after) == len(comments_before) + 1
    new_comment = set(comments_after) - set(comments_before)
    assert new_comment, "Новый комментарий не был создан"
    new_comment = new_comment.pop()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == not_author
    assert new_comment.news.id == new_comment.news.id


def test_user_cant_use_bad_words(news_url, not_author_client):
    response = not_author_client.post(news_url, data=BAD_WORDS_FIXTURE)
    comments_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, delete_url, news_url, comment
):
    comments_before = list(Comment.objects.all())
    response = author_client.delete(delete_url)
    comments_after = list(Comment.objects.all())
    assertRedirects(response, f'{news_url}#comments')
    assert len(comments_after) == len(comments_before) - 1
    deleted_comment = set(comments_before) - set(comments_after)
    assert deleted_comment, "Комментарий не был удален"
    deleted_comment = deleted_comment.pop()
    assert deleted_comment == comment


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
        delete_url, admin_client,
):
    comments_before = list(Comment.objects.values_list('id', flat=True))
    response = admin_client.delete(delete_url)
    comments_after = list(Comment.objects.values_list('id', flat=True))
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments_before == comments_after


def test_author_can_edit_comment(author_client, comment, edit_url, news_url):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, f'{news_url}#comments')
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news.id == comment.news.id


def test_user_cant_edit_comment_of_another_user(
    edit_url, comment, not_author_client
):
    original_comment = Comment.objects.get(pk=comment.pk)
    response = not_author_client.post(edit_url, data=FORM_DATA)
    edited_comment = Comment.objects.get(pk=comment.pk)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert edited_comment.text == original_comment.text
    assert edited_comment.author == original_comment.author
    assert edited_comment.created == original_comment.created
    assert edited_comment.news == original_comment.news
