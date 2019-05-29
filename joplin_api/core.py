# coding: utf-8
"""
    Joplin Editor API - https://joplin.cozic.net/api/

    Usage:
    >>> from joplin_api import JoplinApi
    >>> joplin = JoplinApi(token='the token '))
    >>> joplin.ping()  # to check if the service is up
    >>> joplin.get_folders() # to get all the folders
    >>> folder_title = 'Default'
    >>> folder = joplin.create_folder(folder_title) # to create a folder
    >>> folder_id = folder.json()['id']
    >>> # to create a new note
    >>> note_title = 'My title'
    >>> note_body = '# My Title ## My Subtitle my body'
    >>> joplin.create_note(note_title, note_body, folder_id)
    >>> joplin.get_notes() # to get all the notes
    >>> joplin.get_tags() # to get all the tags
"""
# external lib to use async accesses to the webclipper
import requests_async as requests
import json
import logging
from logging import getLogger
logger = getLogger("joplin_api.api")

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
        default_host = 'http://127.0.0.1:{}'.format(
            config.get('JOPLIN_WEBCLIPPER', 41184))
        self.JOPLIN_HOST = config.get('JOPLIN_HOST', default_host)
        self.token = token

    async def query(self, method, path, **payload):
        """
        Do a query to the System API
        :param method: the kind of query to do
        :param path: endpoints url to the API eg 'notes' 'tags' 'folders'
        :param payload: dict with all the necessary things to deal with the API
        :return json data
        """
        if method not in ('get', 'post', 'put', 'delete'):
            raise ValueError('method expected: get, post, put, delete')

        endpoints = ['/notes/', '/folders/', '/tags/', '/resources/', '/ping/']

        if not any(f"{endpoint}" in path for endpoint in endpoints):
            raise ValueError(f'request expected: notes, folders, tags, '
                             f'resources, version or ping but not {path}')

        full_path = self.JOPLIN_HOST + path
        headers = {'Content-Type': 'application/json'}
        params = {'token': self.token}
        res = {}
        logger.info(f'method {method} path {full_path} params {params} '
                    f'payload {payload} headers {headers}')
        if method == 'get':
            res = await requests.get(full_path, params=params)
        elif method == 'post':
            res = await requests.post(full_path, json=payload, params=params)
        elif method == 'put':
            res = await requests.put(full_path, data=json.dumps(payload), params=params, headers=headers)
        elif method == 'delete':
            res = await requests.delete(full_path, params=params)
        logger.info(f'Response of WebClipper {res}')
        return res

    ##############
    # NOTES
    ##############

    async def get_note(self, note_id):
        """
        GET /notes/:id

        get that note
        :param note_id: string
        :return: res: result of the get
        """
        path = f'/notes/{note_id}'
        return await self.query('get', path, **{})

    async def get_notes(self):
        """
        GET /notes

        get the list of all the notes of the joplin profile
        :return: res: result of the get
        """
        return await self.query('get', '/notes/', **{})

    async def get_notes_tags(self, note_id):
        """
        GET /notes/:id/tags

        get all the tags attached to this note
        :return: res: result of the get
        """
        path = f'/notes/{note_id}/tags'
        return await self.query('get', path, **{})

    async def create_note(self, title, body, parent_id, **kwargs):
        """
        POST /notes

        Add a new note
        :param title: string
        :param body: string
        :param parent_id: string id of the parent folder
        :param kwargs: dict of additional data (eg 'tags')
        :return: res: json result of the post
        """
        data = {'title': title,
                'body': body,
                'parent_id': parent_id,
                'author': kwargs.get('author', ''),
                'source_url': kwargs.get('source_url', ''),
                'tags': kwargs.get('tags', ''),
                'is_todo': kwargs.get('is_todo', '')
                }
        return await self.query('post', '/notes/', **data)

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
        is_todo = kwargs.get('is_todo', 0)
        data = {'title': title,
                'body': body,
                'parent_id': parent_id,
                'author': kwargs.get('author', ''),
                'source_url': kwargs.get('source_url', ''),
                'is_todo': is_todo,
                'tags': kwargs.get('tags', ''),
                }
        if is_todo:
            todo_due = kwargs.get('todo_due', 0)
            todo_completed = kwargs.get('todo_completed', 0)
            data['todo_due'] = todo_due
            data['todo_completed'] = todo_completed

        path = f'/notes/{note_id}'
        return await self.query('put', path, **data)

    async def delete_note(self, note_id):
        """
        DELETE /notes/:id

        Delete a note
        :param note_id: string
        :return: res: json result of the delete
        """
        path = f'/notes/{note_id}'
        return await self.query('delete', path, **{})

    ##############
    # FOLDERS
    ##############

    async def get_folder(self, folder_id):
        """
        GET /folders/:id

        get a folder
        :param folder_id: string of the folder id
        :return: res: json result of the get
        """
        path = f'/folders/{folder_id}'
        return await self.query('get', path, **{})

    async def get_folders(self):
        """
        GET /folders

        get the list of all the folders of the joplin profile
        :return: res: json result of the get
        """
        return await self.query('get', '/folders/', **{})

    async def get_folders_notes(self, folder_id):
        """
        GET /folders/:id/notes

        get the list of all the notes of this folder
        :param folder_id: string of the folder id
        :return: res: json result of the get
        """
        path = f'/folders/{folder_id}/notes'
        return await self.query('get', path, **{})

    async def create_folder(self, folder, **kwargs):
        """
        POST /folders

        Add a new folder
        :param folder: name of the folder
        :return: res: json result of the post
        """
        parent_id = kwargs.get('parent_id', 0)
        data = {'title': folder, 'parent_id': parent_id}
        return await self.query('post', '/folders/', **data)

    async def update_folder(self, folder_id, title, **kwargs):
        """
        PUT /folders/:id

        Edit the folder
        :param folder_id: id of the folder to update
        :param title: string name of the folder
        :return: res: json result of the put
        """
        parent_id = kwargs.get('parent_id', 0)
        data = {'title': title, 'parent_id': parent_id}
        path = f'/folders/{folder_id}'
        return await self.query('put', path, **data)

    async def delete_folder(self, folder_id):
        """
        DELETE /folders

        delete a folder
        :param folder_id: string of the folder to delete
        :return: res: json result of the delete
        """
        path = f'/folders/{folder_id}'
        return await self.query('delete', path, **{})

    async def rename_folder(self, folder_id, folder):
        """
        PUT /folders

        Rename the folder
        :param folder_id: id of the folder to update
        :param folder: string name of the folder
        :return: res: json result of the put
        """
        data = {'id': folder_id, 'folder': folder}
        return await self.query('put', '/folders/', **data)

    ##############
    # TAGS
    ##############

    async def get_tag(self, tag_id):
        """
        GET /tags/:id

        get a tag
        :param tag_id: string name of the tag
        :return: res: json result of the get
        """
        path = f'/tags/{tag_id}'
        return await self.query('get', path, **{})

    async def get_tags(self):
        """
        GET /tags

        get the list of all the tags of the joplin profile
        :return: res: json result of the get
        """
        return await self.query('get', '/tags/', **{})

    async def create_tag(self, title):
        """
        POST /tags

        Add a new tag
        :param title: name of the tag
        :return: res: json result of the post
        """
        data = {'title': title}
        return await self.query('post', '/tags/', **data)

    async def update_tag(self, tag_id, title):
        """
        PUT /tags/:id

        Edit the tag
        :param tag_id: string id of the tag to update
        :param title: string tag name
        :return: res: json result of the put
        """
        data = {'title': title}
        path = f'/tags/{tag_id}'
        return await self.query('put', path, **data)

    async def delete_tag(self, tag_id):
        """
        DELETE /tags/:id

        delete a tag
        :param tag_id: string id of the tag to delete
        :return: res: json result of the delete
        """
        path = f'/tags/{tag_id}'
        return await self.query('delete', path, **{})

    async def get_tags_notes(self, tag_id):
        """
        GET /tags/:id/notes

        Gets all the notes with this tag.
        :return: res: json result of the get
        """
        path = f'/tags/{tag_id}/notes'
        return await self.query('get', path, **{})

    async def create_tags_notes(self, note_id, tag):
        """
        POST /tags/:id/notes

        create a tag from a note
        :return: res: json result of the get
        """
        data = {'title': tag}
        path = f'/tags/{note_id}/notes'
        return await self.query('post', path, **data)

    async def delete_tags_notes(self, tag_id, note_id):
        """
        DELETE /tags/:id/notes/:note_id

        delete a tag from a given note
        :param tag_id: string id of the tag to delete from the note
        :param note_id: string id of the note from which drop the tag
        :return: res: json result of the delete
        """
        path = f'/tags/{tag_id}/notes/{note_id}'
        return await self.query('delete', path, **{})

    ##############
    # RESOURCES
    ##############

    async def get_resource(self, resource_id):
        """
        GET /resources/:id

        get a resource
        :param resource_id: string name of the resource
        :return: res: json result of the get
        """
        path = f'/resource_id/{resource_id}'
        return await self.query('get', path, **{})

    async def get_resources(self):
        """
        GET /resources

        get the list of all the resource_id of the joplin profile
        :return: res: json result of the get
        """
        return await self.query('get', 'resources', **{})

    async def create_resource(self, file, **props):
        """
        POST /resources

        Add a new resource
        :param file: string, name of the file
        :param props: dict
        :return: res: json result of the post
        """
        properties = {}
        # title of the resource
        if 'title' in props:
            properties['title'] = props['title']
        # mime of the resource
        if 'mime' in props:
            properties['mime'] = props['mime']

        data = {'filename': file, 'props': properties}

        return await self.query('post', '/resources/', **data)

    async def update_resources(self, resource_id, **props):
        """
        PUT /resources/:id

        Edit a resource
        :param resource_id: string id of the tag to update
        :param props: dict
        :return: res: json result of the put
        """
        properties = {}
        # title of the resource
        if 'title' in props:
            properties['title'] = props['title']
        # mime of the resource
        if 'mime' in props:
            properties['mime'] = props['mime']

        path = f'/resources/{resource_id}'
        return await self.query('put', path, **properties)

    async def download_resources(self, resource_id):
        """
        GET /resources/:id/file

        Download a file
        :param resource_id: string id of the tag to update
        :return: res: json result of the put
        """
        path = f'/resources/{resource_id}/file'
        return await self.query('get', path, **{})

    async def delete_resources(self, resource_id):
        """
        DELETE /resources/:id

        delete a tag
        :param resource_id: string id of the tag to delete
        :return: res: json result of the delete
        """
        path = f'/resources/{resource_id}'
        return await self.query('delete', path, **{})

    ####################
    # PING
    ####################
    async def ping(self):
        """
        GET /ping

        get the status of the JoplinWebClipper service
        :return: res: json result of the request
        """
        res = await self.query('get', '/ping/', **{})
        if res.text != 'JoplinClipperServer':
            raise ConnectionError('WebClipper unavailable. '
                                  'Check "Tools > Webclipper options" '
                                  'if the service is enable')
        return res
