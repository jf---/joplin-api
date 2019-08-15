# Joplin Api

The API of [Joplin Editor](https://joplinapp.org/) in Python 3.6+

## requirements

* python 3.6+
* [httpx](https://github.com/encode/httpx)

## Installation 

```
git clone  https://github.com/foxmask/joplin-api
cd joplin-api 
pip install -e .
```

## Using Joplin API

```
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
>>> joplin.get_notes() # to get all the notes with
>>> joplin.get_tags() # to get all the tags
```

Have a look at `tests/test_folder.py` for more example

## Tests

install pytest by 
```
pip install -r requirements-dev.txt
```
then, before starting the Unit Test, you will need to set the Token line 10 of tests/conftest.py file

and run
```bash
pytest
``` 

