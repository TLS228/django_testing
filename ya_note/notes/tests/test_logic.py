from http import HTTPStatus

from pytils.translit import slugify  # type: ignore

from notes.forms import WARNING
from notes.models import Note
from .common import FixturesForTests


class TestNoteCreation(FixturesForTests):

    def test_user_can_create_note(self):
        notes_before = list(Note.objects.values_list('id', flat=True))
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        notes_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(len(notes_after), len(notes_before) + 1)
        new_note_id = set(notes_after) - set(notes_before)
        self.assertEqual(len(new_note_id), 1)
        new_note = Note.objects.get(id=new_note_id.pop())
        self.assertEqual(new_note.title, self.form_data["title"])
        self.assertEqual(new_note.text, self.form_data["text"])
        self.assertEqual(new_note.slug, self.form_data["slug"])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_before = list(Note.objects.values_list('id', flat=True))
        response = self.client.post(self.ADD_URL, data=self.form_data)
        expected_url = f"{self.LOGIN_URL}?next={self.ADD_URL}"
        self.assertRedirects(response, expected_url)
        notes_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_before, notes_after)

    def test_not_unique_slug(self):
        notes_before = list(Note.objects.values_list('id', 'title',
                                                     'text', 'author', 'slug'))
        self.form_data["slug"] = self.note.slug
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        notes_after = list(Note.objects.values_list('id', 'title',
                                                    'text', 'author', 'slug'))
        self.assertEqual(notes_before, notes_after)
        self.assertFormError(response, "form", "slug",
                             self.note.slug + WARNING)

    def test_empty_slug(self):
        Note.objects.all().delete()
        form_data = self.form_data.copy()
        form_data.pop("slug")
        response = self.author_client.post(self.ADD_URL, data=form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, form_data["title"])
        self.assertEqual(note.text, form_data["text"])
        self.assertEqual(note.slug, slugify(form_data["title"]))
        self.assertEqual(note.author, self.author)

    def test_author_can_edit_note(self):
        original_author = self.note.author
        response = self.author_client.post(self.EDIT_URL, self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note_after_edit = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after_edit.title, self.form_data["title"])
        self.assertEqual(note_after_edit.text, self.form_data["text"])
        self.assertEqual(note_after_edit.slug, self.form_data["slug"])
        self.assertEqual(note_after_edit.author, original_author)

    def test_other_user_cant_edit_note(self):
        response = self.non_author_client.post(self.EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        response = self.author_client.post(self.DELETE_URL)
        self.assertRedirects(response, self.SUCCESS_URL)
        self.assertEqual(Note.objects.count(), notes_count - 1)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_other_user_cant_delete_note(self):
        notes_count = Note.objects.count()
        response = self.non_author_client.post(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
