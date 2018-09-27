# coding: utf-8
"""
    Joplin Editor API

    Usage:
    >>> from joplin_api import JoplinApi
    >>> joplin = JoplinApi()
    >>> joplin.ping()  # to check if the service is up
    >>> joplin.get_folders() # to get all the folders
    >>> folder_title = 'Default'
    >>> folder = joplin.create_folder(folder_title) # to create a folder
    >>> # to create a new note
    >>> note_title = 'My title'
    >>> note_body = '# My Title ## My Subtitle my body'
    >>> joplin.create_note(note_title, note_body, folder['id'])
    >>> joplin.get_notes() # to get all the notes
    >>> joplin.get_tags() # to get all the tags
    >>> joplin.version() # to get the version of joplin
"""
# external lib to use async accesses to the webclipper
import asks
from asks import Session
import logging

__author__ = 'FoxMaSk'
__all__ = ['JoplinApi']

logging.basicConfig(format='%(message)s', level=logging.INFO)


class JoplinApi:

    # joplin webclipper service
    JOPLIN_HOST = ''
    # API token
    token = ''

    def __init__(self, token, **config):
        """
        :param token: string The API token grabbed from the Joplin config page
        :param config: dict for configuration
        """
        # default value if none are provided when initializing JoplinApi()
        default_host = 'http://127.0.0.1:{}/'.format(config.get('JOPLIN_WEBCLIPPER', 41184))
        self.JOPLIN_HOST = config.get('JOPLIN_HOST', default_host)
        self.token = token

    async def query(self, method, path, **params):
        """
        Do a query to the System API
        :param method: the kind of query to do
        :param path: endpoints url to the API eg 'notes' 'tags' 'folders'
        :param params: a dict with all the necessary things to query the API
        :return json data
        """
        if method not in ('get', 'post', 'put', 'delete'):
            raise ValueError('method expected: get, post, put, delete')
        if path not in ('notes', 'folders', 'tags', 'version', 'ping'):
            raise ValueError('request unexpected: should be \'notes\' or \'folders\' or \'tags\'')

        full_path = self.JOPLIN_HOST + path

        # adding the token to the params
        params['token'] = self.token

        res = {}
        if method == 'get':
            res = await asks.get(full_path, params=params)
        elif method == 'post':
            res = asks.post(full_path, params=params)
        elif method == 'put':
            res = asks.put(full_path, params=params)
        elif method == 'delete':
            res = asks.delete(full_path, params=params)
        return res

    ##############
    # NOTES
    ##############

    async def get_notes(self):
        """
        GET /notes

        get the list of all the notes of the joplin profile
        :return: res: result of the get
        """
        return await self.query('get', 'notes', params={})

    async def create_note(self, title, body, parent_id, **kwargs):
        """
        POST /notes

        Add a new note
        :param title: string
        :param body: string
        :param parent_id: string id of the parent folder
        :param kwargs: dict of additional data
        :return: res: json result of the post
        """
        data = {'title': title,
                'body': body,
                'parent_id': parent_id,
                'author': kwargs.get('author', ''),
                'source_url': kwargs.get('source_url', '')
                }
        return await self.query('post', 'notes', params=data)

    async def update_note(self, note_id, title, body, parent_id, **kwargs):
        """
        PUT /notes

        Edit a note
        :param note_id: string note id
        :param title: string
        :param body: string
        :param parent_id: string id of the parent folder
        :param kwargs: dict of additional data
        :return: res: json result of the put
        """
        data = {'id': note_id,
                'title': title,
                'body': body,
                'parent_id': parent_id,
                'author': kwargs.get('author', ''),
                'source_url': kwargs.get('source_url', '')
                }
        return await self.query('put', 'notes', params=data)

    async def delete_note(self, note_id):
        """
        DELETE /notes

        Delete a note
        :param note_id: string
        :return: res: json result of the delete
        """
        data = {'note_id': note_id}
        return await self.query('delete', 'notes', params=data)

    async def copy_note(self, note_id, parent_id):
        """
        PUT /notes

        Copy a note
        :param note_id: string
        :param parent_id: string the id of the folder where the copy will go
        :return: res: json result of the post
        """
        data = {'note_id': note_id, 'parent_id': parent_id}
        return await self.query('put', 'notes', params=data)

    async def move_note(self, note_id, parent_id):
        """
        PUT /notes

        Move a note
        :param note_id: string
        :param parent_id: string the id of the folder where the note will be moved
        :return: res: json result of the post
        """
        data = {'note_id': note_id, 'parent_id': parent_id}
        return await self.query('put', 'notes', params=data)

    async def rename_note(self, note_id, title):
        """
        PUT /notes

        Rename the note
        :param note_id: id of the note
        :param title: string title of the note
        :return: res: json result of the put
        """
        data = {'id': note_id,
                'title': title}
        return await self.query('put', 'notes', params=data)

    ##############
    # TASKS
    ##############

    async def toggle(self, note_id):
        """
        PUT /tasks

        Toggle a note to task or task to note
        :param note_id: string
        :return: res: json result of the post
        """
        data = {'note_id': note_id}
        return await self.query('put', 'tasks', params=data)

    async def task_clear(self, note_id):
        """
        PUT /tasks

        Clear a task
        :param note_id: string
        :return: res: json result of the post
        """
        data = {'note_id': note_id}
        return await self.query('put', 'tasks', params=data)

    async def task_done(self, note_id):
        """
        PUT /tasks

        Set a task as done
        :param note_id: string
        :return: res: json result of the post
        """
        data = {'note_id': note_id}
        return await self.query('put', 'tasks', params=data)

    async def task_undone(self, note_id):
        """
        PUT /tasks

        Undone a task
        :param note_id: string
        :return: res: json result of the post
        """
        data = {'note_id': note_id}
        return await self.query('put', 'tasks', params=data)

    ##############
    # FOLDERS
    ##############

    async def get_folder(self, folder_id):
        """
        GET /folders

        get a folder
        :param folder_id: string of the folder id
        :return: res: json result of the get
        """
        data = {'parent_id': folder_id}
        return await self.query('get', 'folders', params=data)

    async def get_folders(self):
        """
        GET /folders

        get the list of all the folders of the joplin profile
        :return: res: json result of the get
        """
        return await self.query('get', 'folders', params={})

    async def create_folder(self, folder, **kwargs):
        """
        POST /folders

        Add a new folder
        :param folder: name of the folder
        :return: res: json result of the post
        """
        parent_id = kwargs.get('parent_id', 0)
        data = {'folder': folder,
                'parent_id': parent_id}
        return await self.query('post', 'folders', params=data)

    async def update_folder(self, folder_id, folder, **kwargs):
        """
        PUT /folders

        Edit the folder
        :param folder_id: id of the folder to update
        :param folder: string name of the folder
        :return: res: json result of the put
        """
        parent_id = kwargs.get('folder_id', 0)
        data = {'id': folder_id,
                'folder': folder,
                'parent_id': parent_id}
        return await self.query('put', 'folders', params=data)

    async def delete_folder(self, parent_id):
        """
        DELETE /folders

        delete a folder
        :param parent_id: string of the folder to delete
        :return: res: json result of the delete
        """
        data = {'parent_id': parent_id}
        return await self.query('delete', 'folders', params=data)

    async def rename_folder(self, folder_id, folder):
        """
        PUT /folders

        Rename the folder
        :param folder_id: id of the folder to update
        :param folder: string name of the folder
        :return: res: json result of the put
        """
        data = {'id': folder_id,
                'folder': folder}
        return await self.query('put', 'folders', params=data)

    ##############
    # TAGS
    ##############

    async def get_tag(self, tag):
        """
        GET /tags

        get a tag
        :param tag: name of the tag
        :return: res: json result of the get
        """
        data = {'tag': tag}
        return await self.query('get', 'tags', params=data)

    async def get_tags(self):
        """
        GET /tags

        get the list of all the tags of the joplin profile
        :return: res: json result of the get
        """
        return await self.query('get', 'tags', params={})

    async def create_tag(self, tag):
        """
        POST /tags

        Add a new tag
        :param tag: name of the tag
        :return: res: json result of the post
        """
        data = {'tag': tag}
        return await self.query('post', 'folders', params=data)

    async def update_tag(self, tag, new_tag):
        """
        PUT /tags

        Edit the tag
        :param tag: string name of the tag to update
        :param new_tag: string new name of the tag
        :return: res: json result of the put
        """
        data = {'tag': tag, 'new_tag': new_tag}
        return await self.query('put', 'tags', params=data)

    async def delete_tag(self, tag):
        """
        DELETE /tags

        delete a tag
        :param tag: string name of the tag to delete
        :return: res: json result of the delete
        """
        data = {'tag': tag}
        return await self.query('delete', 'tags', params=data)

    ###################
    # VERSION OF JOPLIN
    ###################
    async def version(self):
        """
        GET /version

        get the version of Joplin
        :return: res: json result of the request
        """
        return await self.query('get', 'version', params={})

    ####################
    # PING
    ####################
    async def ping(self):
        """
        GET /ping

        get the status of the JoplinWebClipper service
        :return: res: json result of the request
        """
        res = await self.query('get', 'ping', params={})
        if res.text != 'JoplinClipperServer':
            raise ConnectionError('WebClipper unavailable. Check "Tools > Webclipper options" if the service is enable')
        return res
