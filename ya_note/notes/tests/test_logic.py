from http import HTTPStatus

from pytils.translit import slugify  # type: ignore

from notes.forms import WARNING
from notes.models import Note
from .common import FixturesForTests, TestURLs


class TestNoteCreation(FixturesForTests, TestURLs):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.expected_url = f"{cls.LOGIN_URL}?next={cls.ADD_URL}"

    def test_user_can_create_note(self):
        self.create_note_and_check_fields(self.form_data,
                                          self.form_data["slug"])

    def create_note_and_check_fields(self, form_data, expected_slug=None):
        Note.objects.all().delete()
        response = self.author_client.post(self.ADD_URL, data=form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note = Note.objects.latest('id')
        self.assertEqual(note.title, form_data["title"])
        self.assertEqual(note.text, form_data["text"])
        self.assertEqual(note.slug,
                         expected_slug or slugify(form_data["title"]))
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.values_list('id', flat=True))
        response = self.client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.expected_url)
        self.assertEqual(notes, set(Note.objects.values_list('id', flat=True)))

    def test_not_unique_slug(self):
        notes_before = list(Note.objects.values_list('id', flat=True))
        self.form_data["slug"] = self.note.slug
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        notes_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_before, notes_after)
        self.assertFormError(response,
                             "form", "slug",
                             self.note.slug + WARNING)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.EDIT_URL, self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note_after_edit = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after_edit.title, self.form_data["title"])
        self.assertEqual(note_after_edit.text, self.form_data["text"])
        self.assertEqual(note_after_edit.slug, self.form_data["slug"])
        self.assertEqual(note_after_edit.author, self.note.author)

    def test_empty_slug(self):
        form_data = self.form_data.copy()
        del form_data["slug"]
        self.create_note_and_check_fields(form_data,
                                          slugify(form_data["title"]))

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
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
