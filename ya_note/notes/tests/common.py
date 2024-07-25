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
        cls.form_data_edited = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'New_note_slug'
        }
        cls.LIST_URL = reverse('notes:list')
        cls.ADD_URL = reverse('notes:add')
        cls.SUCCESS_URL = reverse('notes:success')
        cls.EDIT_URL = reverse('notes:edit', args=[cls.note.slug])
        cls.DELETE_URL = reverse('notes:delete', args=[cls.note.slug])
        cls.LOGIN_URL = reverse('users:login')


class TestURLs:
    URL_ADD = reverse('notes:add')
    URL_DETAIL = reverse('notes:detail', args=[NOTE_SLUG])
    URL_EDIT = reverse('notes:edit', args=[NOTE_SLUG])
    URL_HOME = reverse('notes:home')
    URL_DELETE = reverse('notes:delete', args=[NOTE_SLUG])
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_LIST = reverse('notes:list')
    URL_SIGNUP = reverse('users:signup')
    URL_SUCCESS = reverse('notes:success')
    LOGIN_URL = reverse('users:login')
