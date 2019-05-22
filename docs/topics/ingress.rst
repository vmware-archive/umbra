=======================
Writing Ingress Plugins
=======================

Umbra uses the venerable Plugin Oriented Programing paradigm as it is realized
in the `pop` framework. This means that all of the features of `pop` are
available.

Making an ingress plugin is easy, just add the plugin to `umbra/mods/ingress`.
The `ingress` plugin subsystem only takes a single function, `run`. This can be
a function of any type, a generator, a coroutine, an async generator or a
standard function. The type of function you choose to implement defines how the
ingress system will run. If the ingress system needs to be running continuously
then an async generator is optimal.

This is a simple example of using a subprocess to tail a file. This example shows
how to use subprocess with asyncio in python to shell out to an event stream. There
are better ways to do what we are doing here, but this is a good example of using
subprocess to stream, as it is often a great way to ingest data.

.. code-block:: python

    import asyncio
    import json

    async def run(hub):
        '''
        Shell out salt-run and send in the events from the salt event bus
        '''
        proc = await asyncio.create_subprocess_shell(
                'salt-run state.event',
                stdout=asyncio.subprocess.PIPE)
        while True:
            line = await proc.stdout.readline()
            line = line.decode()
            comps = line.split(maxsplit=1)
            if len(comps) < 2:
                continue
            tag = comps[0].strip()
            data = json.loads(comps[1])
            group = {}
            for pipe in conf:
                group[pipe] = []
            for pipe in conf:
                for match in conf[pipe]:
                    if fnmatch.fnmatch(tag, match):
                        data = json.loads(comps[1].strip())
                        event = {'tag': tag, 'data': data}
                        group[pipe].append(event)
            for pipe in group:
                yield {'pipe': pipe, 'data': group[pipe]}

This example shows how to easily use asyncio subprocess to await lines by line
feedback and yield the formatted ingestion data. This approach can work with
virtually any shell program that continuously emits data.
