import pytest
from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

BAD_WORDS_FIXTURE = [
    {'text': f'Текст раз, {bad_word}, и дальше'} for bad_word in BAD_WORDS
]
FORM_DATA = {'text': 'Новый'}

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(news_url, client):
    comments = set(Comment.objects.values_list('id', flat=True))
    assert client.post(
        news_url, data=FORM_DATA
    ).status_code == HTTPStatus.FOUND
    assert comments == set(
        Comment.objects.values_list('id', flat=True)
    )


def test_user_can_create_comment(not_author_client, news_url,
                                 not_author, news):
    comments_before = set(Comment.objects.all())
    response = not_author_client.post(news_url, data=FORM_DATA)
    comments_after = set(Comment.objects.all())
    assertRedirects(response, f'{news_url}#comments')
    new_comments = comments_after - comments_before
    assert len(new_comments) == 1
    new_comment = new_comments.pop()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == not_author
    assert new_comment.news == news


@pytest.mark.parametrize('bad_word_fixture', BAD_WORDS_FIXTURE)
def test_user_cant_use_bad_words(news_url,
                                 not_author_client, bad_word_fixture):
    response = not_author_client.post(news_url, data=bad_word_fixture)
    comments_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url,
                                   news_url, comment):
    comments_count_before = Comment.objects.count()
    response = author_client.delete(delete_url)
    comments_count_after = Comment.objects.count()
    assertRedirects(response, f'{news_url}#comments')
    assert comments_count_after == comments_count_before - 1
    assert not Comment.objects.filter(id=comment.id).exists()


def test_anonymous_user_cant_delete(client, comment):
    comments_before = list(Comment.objects.values_list('id', 'text',
                                                       'author', 'news'))
    client.post('news:delete', args=(comment.id,))
    comments_after = list(Comment.objects.values_list('id', 'text',
                                                      'author', 'news'))
    assert comments_before == comments_after


def test_author_can_edit_comment(author_client, comment, edit_url, news_url):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, f'{news_url}#comments')
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cant_edit_comment_of_another_user(edit_url, comment,
                                                not_author_client):
    response = not_author_client.post(edit_url, data=FORM_DATA)
    edited_comment = Comment.objects.get(pk=comment.pk)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert edited_comment.text == comment.text
    assert edited_comment.author == comment.author
    assert edited_comment.news == comment.news
