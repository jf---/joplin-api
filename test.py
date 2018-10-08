import unittest
from joplin_api import JoplinApi


class TestJoplinApi(unittest.TestCase):

    def setUp(self):
        self.joplin = JoplinApi.factory(api_type='Api',
                                        token='Open joplin desktop then menu Tools > webclipper ')

    def test_create_folder(self):
        folder = 'TEST FOLDER1'
        self.assertIs(type(folder), str)
        res = self.joplin.create_folder(folder=folder)
        self.assertTrue(res.status_code == 200)

    def test_get_folders(self):
        res = self.joplin.get_folders()
        self.assertTrue(res.status_code == 200)
        self.assertIsInstance(res.json(), list)

    def test_get_folder(self):
        res = self.joplin.create_folder(folder='MY FOLDER2')
        data = res.json()
        parent_id = data['id']
        res = self.joplin.get_folder(parent_id)
        self.assertTrue(res.status_code == 200)
        self.assertIsInstance(res.json(), dict)

    def test_create_note(self):
        res = self.joplin.create_folder(folder='MY FOLDER3')
        data = res.json()
        parent_id = data['id']

        self.assertIs(type(parent_id), str)
        body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
        self.assertIs(type(body), str)
        kwargs = {'tags': 'tag1, tag2'}
        res = self.joplin.create_note(title="NOTE TEST", body=body, parent_id=parent_id, **kwargs)
        self.assertTrue(res.status_code == 200)

    def test_get_notes(self):
        res = self.joplin.get_notes()
        self.assertTrue(res.status_code == 200)
        self.assertIsInstance(res.json(), list)

    def test_get_note(self):
        res = self.joplin.create_folder(folder='MY FOLDER4')
        data = res.json()
        parent_id = data['id']

        body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
        res = self.joplin.create_note(title="NOTE TEST2", body=body, parent_id=parent_id)
        data = res.json()
        note_id = data['id']

        self.assertIs(type(note_id), str)
        res = self.joplin.get_note(note_id)
        self.assertTrue(res.status_code == 200)
        self.assertIsInstance(res.json(), dict)

    def test_get_tags(self):
        res = self.joplin.get_tags()
        self.assertTrue(res.status_code == 200)
        self.assertIsInstance(res.json(), list)

    def test_get_tag(self):
        title = 'TAG TEST'
        res = self.joplin.create_tag(title=title)
        data = res.json()
        tag_id = data['id']

        self.assertIs(type(tag_id), str)
        res = self.joplin.get_tag(tag_id)
        self.assertTrue(res.status_code == 200)
        self.assertIsInstance(res.json(), dict)


if __name__ == '__main__':
    unittest.main()
