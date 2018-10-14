import unittest
from joplin_api import JoplinApi


class TestJoplinApi(unittest.TestCase):

    def setUp(self):
        token = '5fa5a79fdd9feb428297b32b8ebfb92160b95678d6a05b7823df19212046106e89c71e3674df7b8c60ee47c53469cfe3cb4c8b9a174cde5960fabc9186503ae4'
        self.joplin = JoplinApi(token=token)

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
        res = self.joplin.create_note(title="NOTE TEST", body=body,
                                      parent_id=parent_id, **kwargs)
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
        res = self.joplin.create_note(title="NOTE TEST2", body=body,
                                      parent_id=parent_id)
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


if __name__ == '__main__':
    unittest.main()
