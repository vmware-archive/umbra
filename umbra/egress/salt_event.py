# import python libs
import asyncio
import json


async def run(hub, pipe, data):
    '''
    Emit events onto the salt event bus that signal umbra predictions
    '''
    tag = f'umbra/{pipe}'
    for comp in data:
        proc = await asyncio.create_subprocess_shell(
            f'salt-run event.send {tag} \'{json.dumps(comp)}\'',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await proc.wait()