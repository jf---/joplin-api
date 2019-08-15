import pytest
from joplin_api import JoplinApi


@pytest.mark.asyncio
async def test_ping(get_token):
    joplin = JoplinApi(token=get_token)

    ping = await joplin.ping()
    assert type(ping.text) is str
    assert ping.status_code == 200
