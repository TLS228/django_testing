from http.client import NOT_FOUND, OK

from django.contrib.auth import get_user_model  # type: ignore


from .common import FixturesForTests, Routes


User = get_user_model()


class TestRoutes(FixturesForTests):

    def test_pages_availability(self):
        variants = (
            (Routes.URL_HOME, self.client, OK),
            (Routes.URL_LOGIN, self.client, OK),
            (Routes.URL_LOGOUT, self.client, OK),
            (Routes.URL_SIGNUP, self.client, OK),
            (Routes.URL_EDIT, self.author_client, OK),
            (Routes.URL_EDIT, self.reader_client, NOT_FOUND),
            (Routes.URL_DELETE, self.author_client, OK),
            (Routes.URL_DELETE, self.reader_client, NOT_FOUND),
            (Routes.URL_DETAIL, self.author_client, OK),
            (Routes.URL_DETAIL, self.reader_client, NOT_FOUND),
            (Routes.URL_ADD, self.author_client, OK),
            (Routes.URL_SUCCESS, self.author_client, OK),
            (Routes.URL_LIST, self.author_client, OK),
            (Routes.URL_LIST, self.reader_client, OK),
        )
        for url, client, expected_status in variants:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirects_for_anonymous_user(self):
        urls = (
            Routes.URL_LIST,
            Routes.URL_SUCCESS,
            Routes.URL_ADD,
            Routes.URL_DETAIL,
            Routes.URL_EDIT,
            Routes.URL_DELETE,
        )
        login_url = Routes.URL_LOGIN
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    f'{login_url}?next={url}'
                )
