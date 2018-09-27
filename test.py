import asks
import curio

from joplin_api import JoplinApi


async def listall():
    joplin = JoplinApi(token='ABCDEF')
    res = await joplin.get_folders()
    for r in res.json():
        print("folder name : {}".format(r['title']))
    res = await joplin.get_notes()
    for r in res.json():
        print("note title : {}".format(r['title']))
    res = await joplin.get_tags()
    for r in res.json():
        print("tag : {}".format(r['title']))


asks.init('curio')
curio.run(listall())
