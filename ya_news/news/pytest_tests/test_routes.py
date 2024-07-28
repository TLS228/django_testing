import pytest
from http import HTTPStatus

from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_fixture, client_fixture, expected_status',
    [
        ('home_url', 'client', HTTPStatus.NOT_FOUND),
        ('login_url', 'client', HTTPStatus.NOT_FOUND),
        ('logout_url', 'client', HTTPStatus.NOT_FOUND),
        ('signup_url', 'client', HTTPStatus.NOT_FOUND),
        ('news_detail_url', 'client', HTTPStatus.NOT_FOUND),
        ('url_to_delete_comment', 'admin_client', HTTPStatus.NOT_FOUND),
        ('url_to_edit_comment', 'author_client', HTTPStatus.NOT_FOUND),
    ]
)
def test_page_availability(url_fixture, client_fixture,
                           expected_status, request):
    assert request.getfixturevalue(client_fixture
                                   ).get(url_fixture
                                         ).status_code == expected_status


@pytest.mark.parametrize(
    "get_url, expected_redirect_url",
    (
        (pytest.lazy_fixture("get_url_comment_edit"),
         pytest.lazy_fixture("redirect_edit_url")),
        (pytest.lazy_fixture("get_url_comment_delete"),
         pytest.lazy_fixture("redirect_delete_url")),
    ),
)
def redirect_to_login_from_comments(get_url, expected_redirect_url, client):
    assertRedirects(client.get(get_url), expected_redirect_url)
