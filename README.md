# Joplin Api

The API of [Joplin Editor](https://joplinapp.org/) in Python 3.6+

## requirements

* python 3.6+
* [requests-async](https://github.com/encode/requests-async)

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
>>> ping = await joplin.ping()  # to check if the service is up
>>> print(ping.text)
>>> res = await joplin.get_folders() # to get all the folders
>>> print(res.json())
>>> folder_title = 'Default'
>>> res = await joplin.create_folder(folder_title) # to create a folder
>>> folder_id = res.json()['id']
>>> # to create a new note
>>> note_title = 'My title'
>>> note_body = '# My Title ## My Subtitle my body'
>>> kwargs = {'tags': 'tag1, tag2'}
>>> res = await joplin.create_note(title=note_title, body=note_body, parent_id=folder_id, **kwargs)
>>> res = await joplin.get_notes() # to get all the notes
>>> print(res.json())
>>> res = await joplin.get_tags() # to get all the tags
>>> print(res.json())
```

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

