from http.client import FOUND, NOT_FOUND, OK
from random import choice

from django.urls import reverse

import pytest

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_unauthorized_user_can_not_create_comment(
    client,
    news,
    post_comment
):
    count_before_creating = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=post_comment)
    response.status_code == FOUND
    assert Comment.objects.count() == count_before_creating


def test_authorized_user_can_create_comment(
    author,
    author_client,
    news,
    post_comment
):
    count_before_creating = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=post_comment)
    assert response.status_code == FOUND
    count_after_creating = Comment.objects.count()
    assert count_after_creating == 1 + count_before_creating
    comment = Comment.objects.get()
    assert comment.text == post_comment['text']
    assert comment.news == news
    assert comment.author == author


def test_user_can_not_use_bad_words(author_client, news):
    count_before_creating = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    comment_with_bad_words = {
        'text': f'Комментарий с запрещенным словом {choice(BAD_WORDS)}!'
    }
    response = author_client.post(url, data=comment_with_bad_words)
    assert response.status_code == OK
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == count_before_creating


def test_author_can_delete_comment(author_client, news, comment):
    count_before_creating = Comment.objects.count()
    detail_url = reverse('news:detail', args=(news.id,))
    delete_comment_url = reverse('news:delete', args=(comment.id,))
    url_to_comment = detail_url + '#comments'
    response = author_client.delete(delete_comment_url)
    assert response.status_code == FOUND
    assertRedirects(response, url_to_comment)
    count_after_creating = Comment.objects.count()
    assert count_after_creating == count_before_creating - 1


def test_user_can_not_delete_comment_of_user(admin_client, comment):
    count_before_creating = Comment.objects.count()
    delete_comment_url = reverse('news:delete', args=(comment.id,))
    response = admin_client.delete(delete_comment_url)
    assert response.status_code == NOT_FOUND
    count_after_creating = Comment.objects.count()
    assert count_after_creating == count_before_creating


@pytest.mark.django_db
def test_unauthorized_user_can_not_delete_comment(client, comment):
    count_before_creating = Comment.objects.count()
    delete_comment_url = reverse('news:delete', args=(comment.id,))
    response = client.delete(delete_comment_url)
    assert response.status_code == FOUND
    count_after_creating = Comment.objects.count()
    assert count_after_creating == count_before_creating


def test_author_can_edit_comment(
    author_client,
    comment,
    news,
    post_comment
):
    count_before_creating = Comment.objects.count()
    detail_url = reverse('news:detail', args=(news.id,))
    edit_comment_url = reverse('news:edit', args=(comment.id,))
    url_to_comments = detail_url + '#comments'
    response = author_client.post(edit_comment_url, data=post_comment)
    assert response.status_code == FOUND
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == post_comment['text']
    count_after_creating = Comment.objects.count()
    assert count_after_creating == count_before_creating


def test_user_can_not_edit_comment_of_another_user(
    admin_client,
    comment,
    post_comment
):
    count_before_creating = Comment.objects.count()
    edit_comment_url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(edit_comment_url, data=post_comment)
    assert response.status_code == NOT_FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == comment.text
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
    count_after_creating = Comment.objects.count()
    assert count_after_creating == count_before_creating


@pytest.mark.django_db
def test_unauthorized_user_can_not_edit_comment(client, comment, post_comment):
    count_before_creating = Comment.objects.count()
    edit_comment_url = reverse('news:edit', args=(comment.id,))
    current_comment_text = comment.text
    response = client.post(edit_comment_url, data=post_comment)
    assert response.status_code == FOUND
    comment.refresh_from_db()
    assert comment.text == current_comment_text
    count_after_creating = Comment.objects.count()
    assert count_after_creating == count_before_creating
