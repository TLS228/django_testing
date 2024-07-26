from notes.forms import NoteForm
from .common import FixturesForTests, TestURLs


class TestNotesContent(FixturesForTests, TestURLs):

    def test_note_visibility_for_author(self):
        response = self.author_client.get(self.URL_LIST)
        notes = response.context['object_list']
        self.assertEqual(notes.filter(id=self.note.id).count(), 1)
        note_in_list = notes.get(id=self.note.id)
        self.assertEqual(note_in_list.title, self.note.title)
        self.assertEqual(note_in_list.text, self.note.text)
        self.assertEqual(note_in_list.slug, self.note.slug)
        self.assertEqual(note_in_list.author, self.note.author)

    def test_note_visibility_for_non_author(self):
        self.assertNotIn(
            self.note,
            self.non_author_client.get(self.URL_LIST).context['object_list']
        )

    def test_form_presence_on_pages(self):
        for url in [self.ADD_URL, self.EDIT_URL]:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
