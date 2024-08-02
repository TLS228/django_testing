import pytest
from http import HTTPStatus

from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db

URL_HOME = pytest.lazy_fixture('home_url')
URL_DETAIL = pytest.lazy_fixture('news_url')
URL_LOGIN = pytest.lazy_fixture('url_user_login')
URL_LOGOUT = pytest.lazy_fixture('url_logout')
URL_SIGNUP = pytest.lazy_fixture('url_signup')
URL_DEL = pytest.lazy_fixture('delete_url')
URL_EDIT = pytest.lazy_fixture('edit_url')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
ANONYMOUS_CLIENT = pytest.lazy_fixture('client')
REDIRECT_EDIT_URL = pytest.lazy_fixture('redirect_edit_url')
REDIRECT_DEL_URL = pytest.lazy_fixture('redirect_delete_url')


@pytest.mark.parametrize(
    'url_fixture, client_fixture, expected_status',
    (
        (URL_HOME, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_DETAIL, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_LOGIN, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_LOGOUT, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_EDIT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_DEL, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_EDIT, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_DEL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_EDIT, ANONYMOUS_CLIENT, HTTPStatus.FOUND),
        (URL_DEL, ANONYMOUS_CLIENT, HTTPStatus.FOUND),
    ),
)
def test_availability_for_comment_edit_and_delete(expected_status,
                                                  client_fixture,
                                                  url_fixture):
    assert client_fixture.get(url_fixture).status_code == expected_status


@pytest.mark.parametrize(
    "get_url, expected_redirect_url",
    (
        (URL_EDIT,
         REDIRECT_EDIT_URL),
        (URL_DEL,
         REDIRECT_DEL_URL),
    ),
)
def redirect_to_login_from_comments(get_url, expected_redirect_url, client):
    assertRedirects(client.get(get_url), expected_redirect_url)
