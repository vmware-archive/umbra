======================
Writing Egress Plugins
======================

Egress plugins might be the easiest things to write. Just need to take the
data refined by the data plugin and send it somewhere. The `egress` function will
be called with each batch of data that gest sent out. The function is called `run`
and needs to be a coroutine function.

.. code-block:: python

    import pprint


    async def run(hub, pipe, data):
        '''
        Print the egress data pipe to the cli
        '''
        for comp in data:
            pprint.pprint(comp)

This example is amazingly simple, but all you need to to is accept the pipe and the
data and send that data somewhere.

As always, accpet the `hub` as the first argument so you have access to all of the
data and plugins.