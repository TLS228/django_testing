import pytest

from http import HTTPStatus

from django.urls import reverse

from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "name",
    ("news:home", "users:login", "users:logout", "users:signup")
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "get_url, parametrized_client, expected_status",
    (
        (pytest.lazy_fixture("edit_url"),
         pytest.lazy_fixture("author_client"), HTTPStatus.OK),
        (pytest.lazy_fixture("edit_url"),
         pytest.lazy_fixture("not_author_client"), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture("delete_url"),
         pytest.lazy_fixture("author_client"), HTTPStatus.OK),
        (pytest.lazy_fixture("delete_url"),
         pytest.lazy_fixture("not_author_client"), HTTPStatus.NOT_FOUND),
    ),
)
def test_edit_delete_comment_for_different_users(get_url,
                                                 parametrized_client,
                                                 expected_status):
    response = parametrized_client.get(get_url)
    assert response.status_code == expected_status


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
