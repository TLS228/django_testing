from http.client import FOUND, NOT_FOUND, OK

from django.contrib.auth import get_user_model  # type: ignore

from .common import FixturesForTests, TestURLs


User = get_user_model()


class TestRoutes(FixturesForTests, TestURLs):

    def test_pages_availability(self):
        variants = (
            (self.URL_HOME, self.client, OK),
            (self.URL_LOGIN, self.client, OK),
            (self.URL_LOGOUT, self.client, OK),
            (self.URL_SIGNUP, self.client, OK),
            (self.URL_EDIT, self.author_client, OK),
            (self.URL_EDIT, self.reader_client, NOT_FOUND),
            (self.URL_DELETE, self.author_client, OK),
            (self.URL_DELETE, self.reader_client, NOT_FOUND),
            (self.URL_DETAIL, self.author_client, OK),
            (self.URL_DETAIL, self.reader_client, NOT_FOUND),
            (self.ADD_URL, self.author_client, OK),
            (self.URL_SUCCESS, self.author_client, OK),
            (self.URL_LIST, self.author_client, OK),
            (self.URL_LIST, self.reader_client, OK),
            (self.URL_EDIT, self.client, FOUND),
            (self.URL_DELETE, self.client, FOUND),
            (self.URL_DETAIL, self.client, FOUND),
            (self.ADD_URL, self.client, FOUND),
        )
        for url, client, expected_status in variants:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirects_for_anonymous_user(self):
        urls_redirects = (
            (self.URL_LIST, self.REDIRECT_LIST),
            (self.URL_SUCCESS, self.REDIRECT_SUCCESS),
            (self.ADD_URL, self.REDIRECT_ADD),
            (self.URL_DETAIL, self.REDIRECT_DETAIL),
            (self.URL_EDIT, self.REDIRECT_EDIT),
            (self.URL_DELETE, self.REDIRECT_DELETE),
        )
        for url, redirect in urls_redirects:
            with self.subTest():
                self.assertRedirects(
                    self.client.get(url),
                    redirect
                )
