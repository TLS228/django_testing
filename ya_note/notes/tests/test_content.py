from .common import FixturesForTests, Routes
from notes.forms import NoteForm


class TestDetailNote(FixturesForTests):

    def test_user_notes_list(self):
        note_in_list_for_user = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for user, note_in_list in note_in_list_for_user:
            response = user.get(Routes.URL_LIST)
            object_list = response.context['object_list']
            self.assertIs(self.note in object_list, note_in_list)

    def test_add_and_edit_forms(self):
        urls = (
            (Routes.URL_ADD),
            (Routes.URL_EDIT),
        )
        for url in urls:
            response = self.author_client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
