from http.client import FOUND, NOT_FOUND, OK

from django.contrib.auth import get_user_model  # type: ignore


from .common import FixturesForTests, TestURLs


User = get_user_model()


class TestRoutes(FixturesForTests):

    def test_pages_availability(self):
        variants = (
            (TestURLs.URL_HOME, self.client, OK),
            (TestURLs.URL_LOGIN, self.client, OK),
            (TestURLs.URL_LOGOUT, self.client, OK),
            (TestURLs.URL_SIGNUP, self.client, OK),
            (TestURLs.URL_EDIT, self.author_client, OK),
            (TestURLs.URL_EDIT, self.reader_client, NOT_FOUND),
            (TestURLs.URL_DELETE, self.author_client, OK),
            (TestURLs.URL_DELETE, self.reader_client, NOT_FOUND),
            (TestURLs.URL_DETAIL, self.author_client, OK),
            (TestURLs.URL_DETAIL, self.reader_client, NOT_FOUND),
            (TestURLs.ADD_URL, self.author_client, OK),
            (TestURLs.URL_SUCCESS, self.author_client, OK),
            (TestURLs.URL_LIST, self.author_client, OK),
            (TestURLs.URL_LIST, self.reader_client, OK),
            (TestURLs.URL_EDIT, self.client, FOUND),
            (TestURLs.URL_DELETE, self.client, FOUND),
            (TestURLs.URL_DETAIL, self.client, FOUND),
            (TestURLs.ADD_URL, self.client, FOUND),
        )
        for url, client, expected_status in variants:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirects_for_anonymous_user(self):
        urls = (
            TestURLs.URL_LIST,
            TestURLs.URL_SUCCESS,
            TestURLs.ADD_URL,
            TestURLs.URL_DETAIL,
            TestURLs.URL_EDIT,
            TestURLs.URL_DELETE,
        )
        login_url = TestURLs.URL_LOGIN
        redirect_urls = {url: f'{login_url}?next={url}' for url in urls}
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_urls[url]
                )
