import asks
import curio

from joplin_api import JoplinApi


async def listall():
    joplin = JoplinApi()
    res = await joplin.get_folders()
    for r in res.json():
        print("folder name : {}".format(r['title']))

asks.init('curio')
curio.run(listall())
