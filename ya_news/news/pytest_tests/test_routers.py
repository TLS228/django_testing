from http.client import OK, NOT_FOUND

from pytest_django.asserts import assertRedirects
import pytest

from .common import Urls

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client_type, status_code',
    ((Urls.HOME_URL, Urls.ANY_USER, OK),
     (Urls.DETAIL_URL, Urls.ANY_USER, OK),
     (Urls.LOGIN_URL, Urls.ANY_USER, OK),
     (Urls.LOGOUT_URL, Urls.ANY_USER, OK),
     (Urls.SIGNUP_URL, Urls.ANY_USER, OK),
     (Urls.EDIT_URL, Urls.READER, NOT_FOUND),
     (Urls.EDIT_URL, Urls.AUTHOR, OK),
     (Urls.DELETE_URL, Urls.READER, NOT_FOUND),
     (Urls.DELETE_URL, Urls.AUTHOR, OK))
)
def test_home_availability_for_anonymous_user(url, client_type, status_code):
    response = client_type.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'url',
    (Urls.EDIT_URL, Urls.DELETE_URL)
)
def test_redirects(client, login_url, url):
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
