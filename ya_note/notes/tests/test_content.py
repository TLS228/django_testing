from notes.forms import NoteForm
from .common import FixturesForTests


class TestNotesContent(FixturesForTests):

    def test_note_visibility_for_author(self):
        response = self.author_client.get(self.LIST_URL)
        notes_list = response.context['object_list']
        self.assertIn(self.note, notes_list)
        displayed_note = notes_list.get(id=self.note.id)
        self.assertEqual(displayed_note.title, self.note.title)
        self.assertEqual(displayed_note.text, self.note.text)
        self.assertEqual(displayed_note.slug, self.note.slug)
        self.assertEqual(displayed_note.author, self.note.author)

    def test_note_visibility_for_non_author(self):
        response = self.non_author_client.get(self.LIST_URL)
        notes_list = response.context['object_list']
        self.assertNotIn(self.note, notes_list)

    def test_form_presence_on_pages(self):
        for url in [self.ADD_URL, self.EDIT_URL]:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
