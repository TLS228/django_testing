from django.urls import reverse

import pytest

NEWS_COUNT_ON_HOME_PAGE = 10


class Routes():
    URL_HOME = reverse('news:home')
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_SIGNUP = reverse('users:signup')
    LOGIN_URL = reverse('users:login')


class Urls():
    HOME_URL = pytest.lazy_fixture('home_url')
    LOGIN_URL = pytest.lazy_fixture('login_url')
    LOGOUT_URL = pytest.lazy_fixture('logout_url')
    SIGNUP_URL = pytest.lazy_fixture('signup_url')
    DETAIL_URL = pytest.lazy_fixture('detail_url')
    EDIT_URL = pytest.lazy_fixture('edit_url')
    DELETE_URL = pytest.lazy_fixture('delete_url')
    ANY_USER = pytest.lazy_fixture('client')
    AUTHOR = pytest.lazy_fixture('author_client')
    READER = pytest.lazy_fixture('reader_client')
