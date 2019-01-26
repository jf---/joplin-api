# Joplin Api

The API of [Joplin Editor](https://joplin.cozic.net/) in Python 3.6+

## requirements

* python 3.6+
* [requests](http://docs.python-requests.org/)

## Installation 

```
git clone  https://github.com/foxmask/joplin-api
cd joplin-api 
pip install -e .
```

## Using Joplin API

```
>>> from joplin_api import JoplinApi
>>> joplin = JoplinApi(token='the token provided by Joplin in the WebClipper menu:P'))
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
```

## Tests

before starting the Unit Test, you will need to set the Token line 9 of test.py

token = 'the token found on the webclipper config of joplin desktop'
