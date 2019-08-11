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

with python 3.6.x
```
import asyncio
from joplin_api import JoplinApi


async def ping_me(joplin):
    ping = await joplin.ping()
    return ping


async def main():
    TOKEN = "1blahblubb13db"
    joplin = JoplinApi(token=TOKEN)
    res = await ping_me(joplin)
    print(res.text)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
```

with python 3.7.x

```
import asyncio
from joplin_api import JoplinApi


async def ping_me(joplin):
    ping = await joplin.ping()
    return ping


async def main():
    TOKEN = "1blahblubb13db"
    joplin = JoplinApi(token=TOKEN)
    res = await ping_me(joplin)
    print(res.text)

asyncio.run(main())
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

