from http.client import NOT_FOUND

from pytils.translit import slugify

from .common import FixturesForTests, Routes
from notes.forms import WARNING
from notes.models import Note

TITLE = 'Заголовок'
TEXT = 'Текст'
SLUG = 'note_slug'


class TestCreateNote(FixturesForTests):

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        count_before_creating = Note.objects.count()
        response = self.author_client.post(Routes.URL_ADD, data=self.form_data)
        self.assertRedirects(response, Routes.URL_SUCCESS)
        count_after_creating = Note.objects.count()
        count_difference = count_after_creating - count_before_creating
        self.assertEqual(count_difference, 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, TITLE)
        self.assertEqual(new_note.text, TEXT)
        self.assertEqual(new_note.slug, SLUG)
        self.assertEqual(new_note.author, self.author)

    def test_anon_user_cant_create_note(self):
        count_before_creating = Note.objects.count()
        response = self.client.post(Routes.URL_ADD, data=self.form_data)
        count_after_creating = Note.objects.count()
        count_difference = count_after_creating - count_before_creating
        self.assertEqual(count_difference, 0)
        expected_url = f'{Routes.URL_LOGIN}?next={Routes.URL_ADD}'
        self.assertRedirects(response, expected_url)

    def test_empty_slug(self):
        Note.objects.all().delete()
        count_before_creating = Note.objects.count()
        self.form_data.pop('slug')
        response = self.author_client.post(
            Routes.URL_ADD, data=self.form_data
        )
        self.assertRedirects(response, Routes.URL_SUCCESS)
        count_after_creating = Note.objects.count()
        count_difference = count_after_creating - count_before_creating
        self.assertEqual(count_difference, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestEditDeleteNote(FixturesForTests):
    NEW_TITLE = 'Новый заголовок'
    NEW_TEXT = 'Новый текст'
    NEW_SLUG = 'New_note_slug'

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            Routes.URL_EDIT, data=self.form_data_edited
        )
        self.assertRedirects(response, Routes.URL_SUCCESS)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NEW_TITLE)
        self.assertEqual(self.note.text, self.NEW_TEXT)
        self.assertEqual(self.note.slug, self.NEW_SLUG)

    def test_other_user_cannot_edit_note(self):
        response = self.reader_client.post(
            Routes.URL_EDIT, data=self.form_data_edited
        )
        self.assertEqual(response.status_code, NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, TITLE)
        self.assertEqual(self.note.text, TEXT)
        self.assertEqual(self.note.slug, SLUG)

    def test_author_can_delete_note(self):
        count_before_deletion = Note.objects.count()
        response = self.author_client.delete(Routes.URL_DELETE)
        self.assertRedirects(response, Routes.URL_SUCCESS)
        count_after_deletion = Note.objects.count()
        count_difference = count_before_deletion - count_after_deletion
        self.assertEqual(count_difference, 1)

    def test_other_user_cannot_delete_note(self):
        count_before_deletion = Note.objects.count()
        response = self.reader_client.delete(Routes.URL_DELETE)
        self.assertEqual(response.status_code, NOT_FOUND)
        count_after_deletion = Note.objects.count()
        count_difference = count_before_deletion - count_after_deletion
        self.assertEqual(count_difference, 0)

    def test_slug_cannot_be_repeat(self):
        self.form_data_edited['slug'] = self.note.slug
        count_before_creating = Note.objects.count()
        response = self.author_client.post(
            Routes.URL_ADD, data=self.form_data_edited
        )
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=SLUG + WARNING
        )
        count_after_creating = Note.objects.count()
        count_difference = count_after_creating - count_before_creating
        self.assertEqual(count_difference, 0)
