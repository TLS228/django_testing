from http.client import NOT_FOUND, OK

from .common import FixturesForTests, Routes


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
        for url, client, result in variants:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, result)

    def test_redirects_for_anonymous_user(self):
        urls = (
            Routes.URL_LIST,
            Routes.URL_SUCCESS,
            Routes.URL_ADD,
            Routes.URL_DETAIL,
            Routes.URL_EDIT,
            Routes.URL_DELETE,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{Routes.URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
