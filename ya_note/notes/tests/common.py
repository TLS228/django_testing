from django.contrib.auth import get_user_model  # type: ignore
from django.test import Client, TestCase  # type: ignore
from django.urls import reverse  # type: ignore

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'note_slug'


class FixturesForTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.non_author = User.objects.create(username='non_author')
        cls.author_client = Client()
        cls.non_author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.non_author_client.force_login(cls.non_author)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Test Note',
            text='This is a test note',
            author=cls.author,
            slug=NOTE_SLUG,
        )
        cls.form_data = {
            "title": "Новый заголовок",
            "text": "Новый текст",
            "slug": "New_note_slug",
        }


class TestURLs:
    ADD_URL = reverse('notes:add')
    URL_DETAIL = reverse('notes:detail', args=[NOTE_SLUG])
    URL_EDIT = reverse('notes:edit', args=[NOTE_SLUG])
    URL_HOME = reverse('notes:home')
    URL_DELETE = reverse('notes:delete', args=[NOTE_SLUG])
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_LIST = reverse('notes:list')
    URL_SIGNUP = reverse('users:signup')
    URL_SUCCESS = reverse('notes:success')
    REDIRECT_ADD = f"{URL_LOGIN}?next={ADD_URL}"
    REDIRECT_LIST = f"{URL_LOGIN}?next={URL_LIST}"
    REDIRECT_SUCCESS = f"{URL_LOGIN}?next={URL_SUCCESS}"
    REDIRECT_DETAIL = f"{URL_LOGIN}?next={URL_DETAIL}"
    REDIRECT_EDIT = f"{URL_LOGIN}?next={URL_EDIT}"
    REDIRECT_DELETE = f"{URL_LOGIN}?next={URL_DELETE}"
