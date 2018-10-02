# coding: utf-8
"""
    Joplin Editor API - https://joplin.cozic.net/api/

    Usage:
    >>> from joplin_api import JoplinApi
    >>> joplin = JoplinApi('Api')
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
import requests
import json
import shlex
from subprocess import Popen, PIPE
import logging
from logging import getLogger
logger = getLogger("joplin_api.api")

__author__ = 'FoxMaSk'
__all__ = ['JoplinApi']

logging.basicConfig(format='%(message)s', level=logging.INFO)


class JoplinApi:

    # factory to switch between API in case we do not use WebClipper

    def factory(api_type, token):
        """

        :param api_type: type of API to use
        :param token: string of the unique TOKEN of the API
        :return:
        """
        if api_type == "CmdApi":
            return JoplinCmdApi(token)
        if api_type == "Api":
            return JoplinWebApi(token)
        assert 0, "Bad Joplin API: " + api_type

    factory = staticmethod(factory)


class JoplinWebApi(JoplinApi):

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
        default_host = 'http://127.0.0.1:{}'.format(config.get('JOPLIN_WEBCLIPPER', 41184))
        self.JOPLIN_HOST = config.get('JOPLIN_HOST', default_host)
        self.token = token

    def query(self, method, path, **payload):
        """
        Do a query to the System API
        :param method: the kind of query to do
        :param path: endpoints url to the API eg 'notes' 'tags' 'folders'
        :param payload: a dict with all the necessary things to deal with the API
        :return json data
        """
        if method not in ('get', 'post', 'put', 'delete'):
            raise ValueError('method expected: get, post, put, delete')

        endpoints = ['notes', 'folders', 'tags', 'resources', 'version', 'ping']

        if not any(f"/{endpoint}/" in path for endpoint in endpoints):
            raise ValueError(f'request expected: notes, folders, tags, resources, version or ping but not {path}')

        full_path = self.JOPLIN_HOST + path
        headers = {'Content-Type': 'application/json'}
        params = {'token':  self.token}
        res = {}
        if method == 'get':
            res = requests.get(full_path, params=params)
        elif method == 'post':
            res = requests.post(full_path, json=payload, params=params)
        elif method == 'put':
            res = requests.put(full_path, data=json.dumps(payload), params=params, headers=headers)
        elif method == 'delete':
            res = requests.delete(full_path, params=params)

        return res

    ##############
    # NOTES
    ##############

    def get_note(self, note_id):
        """
        GET /notes/:id

        get that note
        :param note_id: string
        :return: res: result of the get
        """
        path = f'/notes/{note_id}'
        return self.query('get', path, **{})

    def get_notes(self):
        """
        GET /notes

        get the list of all the notes of the joplin profile
        :return: res: result of the get
        """
        return self.query('get', '/notes/', **{})

    def get_notes_tags(self, note_id):
        """
        GET /notes/:id/tags

        get all the tags attached to this note
        :return: res: result of the get
        """
        path = f'/notes/{note_id}/tags'
        return self.query('get', path, **{})

    def create_note(self, title, body, parent_id, **kwargs):
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
        return self.query('post', '/notes/', **data)

    def update_note(self, note_id, title, body, parent_id, **kwargs):
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
                'is_todo': is_todo
                }
        if is_todo:
            todo_due = kwargs.get('todo_due', 0)
            todo_completed = kwargs.get('todo_completed', 0)
            data['todo_due'] = todo_due
            data['todo_completed'] = todo_completed

        path = f'/notes/{note_id}'
        return self.query('put', path, **data)

    def delete_note(self, note_id):
        """
        DELETE /notes/:id

        Delete a note
        :param note_id: string
        :return: res: json result of the delete
        """
        path = f'/notes/{note_id}'
        return self.query('delete', path, **{})

    ##############
    # FOLDERS
    ##############

    def get_folder(self, folder_id):
        """
        GET /folders/:id

        get a folder
        :param folder_id: string of the folder id
        :return: res: json result of the get
        """
        path = f'/folders/{folder_id}'
        return self.query('get', path, **{})

    def get_folders(self):
        """
        GET /folders

        get the list of all the folders of the joplin profile
        :return: res: json result of the get
        """
        return self.query('get', '/folders/', **{})

    def get_folders_notes(self, folder_id):
        """
        GET /folders/:id/notes

        get the list of all the notes of this folder
        :param folder_id: string of the folder id
        :return: res: json result of the get
        """
        path = f'/folders/{folder_id}/notes'
        return self.query('get', path, **{})

    def create_folder(self, folder, **kwargs):
        """
        POST /folders

        Add a new folder
        :param folder: name of the folder
        :return: res: json result of the post
        """
        parent_id = kwargs.get('parent_id', 0)
        data = {'folder': folder, 'parent_id': parent_id}
        return self.query('post', '/folders/', **data)

    def update_folder(self, folder_id, title, **kwargs):
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
        return self.query('put', path, **data)

    def delete_folder(self, folder_id):
        """
        DELETE /folders

        delete a folder
        :param folder_id: string of the folder to delete
        :return: res: json result of the delete
        """
        path = f'/folders/{folder_id}'
        return self.query('delete', path, **{})

    def rename_folder(self, folder_id, folder):
        """
        PUT /folders

        Rename the folder
        :param folder_id: id of the folder to update
        :param folder: string name of the folder
        :return: res: json result of the put
        """
        data = {'id': folder_id, 'folder': folder}
        return self.query('put', '/folders/', **data)

    ##############
    # TAGS
    ##############

    def get_tag(self, tag_id):
        """
        GET /tags/:id

        get a tag
        :param tag_id: string name of the tag
        :return: res: json result of the get
        """
        path = f'/tags/{tag_id}'
        return self.query('get', path, **{})

    def get_tags(self):
        """
        GET /tags

        get the list of all the tags of the joplin profile
        :return: res: json result of the get
        """
        return self.query('get', '/tags/', **{})

    def create_tag(self, title):
        """
        POST /tags

        Add a new tag
        :param title: name of the tag
        :return: res: json result of the post
        """
        data = {'title': title}
        return self.query('post', '/tags/', **data)

    def update_tag(self, tag_id, title):
        """
        PUT /tags/:id

        Edit the tag
        :param tag_id: string id of the tag to update
        :param title: string tag name
        :return: res: json result of the put
        """
        data = {'title': title}
        path = f'/tags/{tag_id}'
        return self.query('put', path, **data)

    def delete_tag(self, tag_id):
        """
        DELETE /tags/:id

        delete a tag
        :param tag_id: string id of the tag to delete
        :return: res: json result of the delete
        """
        path = f'/tags/{tag_id}'
        return self.query('delete', path, **{})

    def get_tags_notes(self, note_id):
        """
        GET /tags/:id/notes

        get the list of all the tags for this note
        :return: res: json result of the get
        """
        path = f'/tags/{note_id}/notes'
        return self.query('get', path, **{})

    def create_tags_notes(self, note_id, tag):
        """
        POST /tags/:id/notes

        create a tag from a note
        :return: res: json result of the get
        """
        data = {'title': tag}
        path = f'/tags/{note_id}/notes'
        return self.query('post', path, **data)

    def delete_tags_notes(self, tag_id, note_id):
        """
        GET /tags/:id/notes/:note_id

        delete a tag from a given note
        :param tag_id: string id of the tag to delete from the note
        :param note_id: string id of the note from which drop the tag
        :return: res: json result of the delete
        """
        path = f'/tags/{tag_id}/notes/{note_id}'
        return self.query('delete', path, **{})

    ##############
    # RESOURCES
    ##############

    def get_resource(self, resource_id):
        """
        GET /resources/:id

        get a resource
        :param resource_id: string name of the resource
        :return: res: json result of the get
        """
        path = f'/resource_id/{resource_id}'
        return self.query('get', path, **{})

    def get_resources(self):
        """
        GET /resources

        get the list of all the resource_id of the joplin profile
        :return: res: json result of the get
        """
        return self.query('get', 'resources', **{})

    def create_resource(self, title, **kwargs):
        """
        POST /resources

        Add a new resource
        :param title: name of the file
        :return: res: json result of the post
        """
        data = {'title': title}
        return self.query('post', '/resources/', **data)

    def update_resources(self, resource_id, title):
        """
        PUT /resources/:id

        Edit a resource
        :param resource_id: string id of the tag to update
        :param title: string title
        :return: res: json result of the put
        """
        data = {'title': title}
        path = f'/resources/{resource_id}'
        return self.query('put', path, **data)

    def download_resources(self, resource_id):
        """
        GET /resources/:id/file

        Download a file
        :param resource_id: string id of the tag to update
        :return: res: json result of the put
        """
        path = f'/resources/{resource_id}/file'
        return self.query('get', path, **{})

    def delete_resources(self, resource_id):
        """
        DELETE /resources/:id

        delete a tag
        :param resource_id: string id of the tag to delete
        :return: res: json result of the delete
        """
        path = f'/resources/{resource_id}'
        return self.query('delete', path, **{})

    ###################
    # VERSION OF JOPLIN
    ###################
    def version(self):
        """
        GET /version

        get the version of Joplin
        :return: res: json result of the request
        """
        return self.query('get', '/version/', **{})

    ####################
    # PING
    ####################
    def ping(self):
        """
        GET /ping

        get the status of the JoplinWebClipper service
        :return: res: json result of the request
        """
        res = self.query('get', 'ping', **{})
        if res.text != 'JoplinClipperServer':
            raise ConnectionError('WebClipper unavailable. Check "Tools > Webclipper options" if the service is enable')
        return res


class JoplinCmdApi(JoplinApi):

    profile_path = ''

    def __init__(self, token='', **config):
        """
        set the profile path of joplin
        """
        self.token = token
        self.profile_path = config.get('JOPLIN_PROFILE_PATH', '')

    def _run(self, line):
        """
        Build the command to be running
        :param line: the command to run
        :return: message and exitcode
        """
        cmd = "joplin --profile {} {}".format(self.profile_path, line)
        logger.debug(cmd)
        args = shlex.split(cmd)
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        logger.info("joplin %s %s %s" % (out, err, exitcode))
        return out, err, exitcode

    #########
    # Notes #
    #########
    def ls(self, type_object):
        """
        list notes, but extract __the line__ of the new created note
        :param type_object: n = note - t = task
        :return: message and exitcode
        """
        line = " ls -n 1 -s created_time -t {} -f json".format(type_object)
        return self._run(line)

    def setp(self, note_id, **kwargs):
        """
        set properties
        :param note_id: id on the created note
        :param kwargs: can contains body and some other additionals properties
        :return: message and exitcode
        """
        out = err = ''
        exitcode = 0
        line_start = 'set {note_id} '.format(note_id=note_id)
        for key in kwargs:
            line = line_start + ' {key} "{value}"'.format(key=key, value=kwargs.get(key))
            logger.debug("SET %s " % line)
            out, err, exitcode = self._run(line)

        return out, err, exitcode

    def create_note(self, notebook, title, body, type_object='n'):
        """
        Create a note
        :param notebook: notebook choosen to store the new note
        :param title: note title to create
        :param body: content of the note to add to the created note
        :param type_object: type of object to create : n = note, t = task
        :return: message and exitcode
        """
        kwargs = dict()
        out, err, exitcode = self._use(notebook)
        if exitcode == 0:
            line = 'mknote "{}"'.format(title)
            out, err, exitcode = self._run(line)
            if exitcode == 0:
                out, err, exitcode = self.ls(type_object)
                if exitcode == 0:
                    # 3) set the body of the note
                    payload = json.loads(out)
                    note_id = payload[0]['id'][:5]
                    logger.debug("note id %s " % note_id)
                    logger.debug("titre %s " % payload[0]['title'])
                    logger.debug("body  %s " % payload[0]['body'])
                    logger.debug("todo  %s " % payload[0]['is_todo'])
                    kwargs['body'] = body
                    out, err, exitcode = self.setp(note_id, **kwargs)
        return out, err, exitcode

    def update_note(self, note_id, parent_id, title, body, is_todo):
        """
        Edit a note
        :param note_id: note id to edit
        :param parent_id: notebook choosen to store the note
        :param title: note title to update
        :param body: content of the note edit the note
        :param is_todo: boolean 1 = todo 0 = note
        :return: message and exitcode
        """
        kwargs = dict()
        kwargs['parent_id'] = parent_id
        kwargs['title'] = title
        kwargs['body'] = body
        kwargs['is_todo'] = is_todo
        return self.setp(note_id, **kwargs)

    # def rmnote(self, note):
    def delete_note(self, note):
        """
        Remove a note
        :param note: id to delete
        :return: message and exitcode
        """
        line = 'rmnote "{}"'.format(note)
        logger.debug(line)
        return self._run(line)

    ############
    # Noteooks #
    ############
    # def mkbook(self, notebook):
    def create_folder(self, notebook):
        """
        Create a notebook
        :param notebook: to create
        :return: message and exitcode
        """
        line = 'mkbook "{}"'.format(notebook)
        logger.debug(line)
        return self._run(line)

    # def rmbook(self, notebook):
    def delete_folder(self, notebook):
        """
        Remove a notebook
        :param notebook: to delete
        :return: message and exitcode
        """
        line = 'rmbook '.format(notebook)
        logger.debug(line)
        return self._run(line)

    def _use(self, notebook):
        """
        point to the notebook to use
        :return: message and exitcode
        """
        line = 'use "{}"'.format(notebook)
        logger.debug(line)
        return self._run(line)

    #########
    # To-do #
    #########
    def toggle(self, note_id):
        """
        set a note as a (uncomplet) To-do
        then set a To-do as complet
        then set a completed To-do as a (uncompleted) To-do
        :return: message and exitcode
        """
        line = 'todo toggle "{}"'.format(note_id)
        logger.debug(line)
        return self._run(line)

    def clear(self, note_id):
        """
        set a To-do back as note
        :return: message and exitcode
        """
        line = 'todo clear "{}"'.format(note_id)
        logger.debug(line)
        return self._run(line)

    def done(self, note_id):
        """
        Marks a to-do as completed.
        :return: message and exitcode
        """
        line = 'done "{}"'.format(note_id)
        logger.debug(line)
        return self._run(line)

    def undone(self, note_id):
        """
        Marks a to-do as non-completed.
        :return: message and exitcode
        """
        line = 'undone "{}"'.format(note_id)
        logger.debug(line)
        return self._run(line)

    ######################
    # Note and Notebooks #
    ######################
    def ren(self, note_or_folder_id, name):
        """
        Rename a note or a folder
        :param note_or_folder_id: id to rename (note or folder)
        :param name: string to use for renaming
        :return: message and exitcode
        """
        line = 'ren "{}" "{}"'.format(note_or_folder_id, name)
        logger.debug(line)
        return self._run(line)

    #######
    # Tag #
    #######
    def tag(self, action, tag_id, note_id):
        """
        deal with tag for a note
        :param action: can be add/remove/list
        :param tag_id: tag to add or remove to the note
        :param note_id: id of the note where the tag is added or deleted
        :return: message and exitcode
        """
        line = "tag {action} {tag_id} {note_id}".format(action=action, tag_id=tag_id, note_id=note_id)
        return self._run(line)

    ###############
    # Joplin info #
    ###############
    def version(self):
        """
        Version of Joplin
        :return: message and exitcode
        """
        logger.debug('joplin version ?')
        return self._run('version')

    ############
    # Settings #
    ############
    def config(self, name, value):
        """
        apply a config for `name` to `value`
        see doc at https://joplin.cozic.net/terminal/  `config [name] [value]`
        :param name: config name
        :param value: value to apply
        :return: message and exitcode
        """
        line = "config {name} {value}".format(name=name, value=value)
        return self._run(line)
