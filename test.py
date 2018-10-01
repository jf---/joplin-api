from joplin_api import JoplinApi


def listfolders():
    joplin = JoplinApi.factory(api_type='Api', token='ABCDEF')
    res = joplin.get_folders()
    for r in res.json():
        print("folder name : {}".format(r['title']))


def listnotes():
    joplin = JoplinApi.factory(api_type='Api', token='a_valid_token')
    res = joplin.get_notes()
    for r in res.json():
        print("note title : {}".format(r['title']))


def listtags():
    joplin = JoplinApi.factory(api_type='Api', token='ABCDEF')
    res = joplin.get_tags()
    for r in res.json():
        print("tag : {}".format(r['title']))


listfolders()
listnotes()
listtags()
