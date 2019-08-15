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

Have a look at `tests/test_folder.py` and `test/test_ping.py` 

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

