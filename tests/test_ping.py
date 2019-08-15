from joplin_api import JoplinApi


def test_ping(get_token):
    joplin = JoplinApi(token=get_token)

    ping = joplin.ping()
    assert type(ping.text) is str
    assert ping.status_code == 200
