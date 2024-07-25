from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class FixturesForTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='note_slug',
        )
        cls.form_data = {'title': 'Заголовок',
                         'text': 'Текст',
                         'slug': 'note_slug'}
        cls.form_data_edited = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'New_note_slug'
        }


class Routes():
    URL_ADD = reverse('notes:add')
    URL_DETAIL = reverse('notes:detail', args=['note_slug'])
    URL_EDIT = reverse('notes:edit', args=['note_slug'])
    URL_HOME = reverse('notes:home')
    URL_DELETE = reverse('notes:delete', args=['note_slug'])
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_LIST = reverse('notes:list')
    URL_SIGNUP = reverse('users:signup')
    URL_SUCCESS = reverse('notes:success')
    LOGIN_URL = reverse('users:login')
