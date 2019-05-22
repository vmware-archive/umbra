====================
Writing Data Plugins
====================

Data plugins are simple, but they do follow a format and expect certain
inputs and outputs. The data functions are executed as new data comes in
and will be executed over and over again. Unlike, for instance, `ingress`
plugins that are only executed once to set up the flow of data.

The data plugin takes 2 functions, both are coroutines. The first function,
`prepare` takes the name of the pipe and the inbound data as a list. The
`prepare` coroutine function needs to return a list of arrays that can be
used by a model.

Prepare Function
================

This example shows how to prepare data formatted in a python dict for
the salt event bus. Remember that Umbra uses `pop` as the plugin system so
the `hub` needs to be accepted as the first argument.

.. code-block:: python

    async def prepare(hub, pipe, inbound):
        '''
        Takes the raw data loaded from a salt event stream, this data is transformed
        into data that can be loaded in to the model and we save the string map dicts
        for future translation
        '''
        ret = []
        d_count = 0
        for event in inbound:
            if not hub.P[pipe]['tmap_populated']:
                for key in event['data']:
                    if not isinstance(event['data'][key], str):
                        # TODO: Make this able to handle more than just strings
                        continue
                    if key == '_stamp':
                        continue
                    hub.P[pipe]['tmap'].append(key)
                hub.P[pipe]['tmap_populated'] = True
            x = [0 for n in hub.P[pipe]['tmap']]
            for key in event['data']:
                if not isinstance(event['data'][key], str):
                    # TODO: Be able to handle more than just strings here
                    continue
                if key == '_stamp':
                    continue
                x[hub.P[pipe]['tmap'].index(key)] = hub.data.init.word_map(
                    event['data'][key],
                    hub.P[pipe]['words'],
                    hub.P[pipe]['r_words'])
            ret.append(x)
        return ret

Since the data preparations need to persist data across runs, this is one of the places
in umbra that we need to use the `hub` which has been given to us by `pop`.

The `hub` is a namespaced hierarchy used to store plugin references and variables.
The `hub` makes it easy to persist data in a clean way across the entire application.
In this case we use the `hub.P` dict that has already been prepared for you. Under
hub.P there is a dict for the pipe we are running in, and this is the place to store
data about this pipe.

With the `hub` already prepared we can store information that we need in future runs, like
the words and reverse words dicts and we use the tmap to line up the correct keys from the
events in the correct locations in the returned number array.

Refine Function
===============

After creating the `prepare` function the `refine` coroutine is also required. The `refine`
coroutine function is the opposite as the `prepare` coroutine function. It takes the data
emitted by the model and reconstitutes it back into the same type of data that was originally
received. This makes it easy to pipeline data in and out.

Here is the `refine` function that goes along with this `prepare function`:


.. code-block:: python

    async def refine(hub, pipe, data, preds):
        '''
        Take the data from the model and refine it back into salt event format
        '''
        dmap = hub.P[pipe]
        rets = []
        for ind in range(len(preds)):
            if not preds[ind]:
                continue
            ret = {}
            for t_ind in range(len(dmap['tmap'])):
                ret[dmap['tmap'][t_ind]] = dmap['r_words'][data[ind][t_ind]]
            rets.append(ret)
        return rets

The refine function takes the pipe, data and predictions. The predictions are the numbers that
map to the dataset. So now we can just go over the dataset, line up the outliers and restore the
data to what it was originally.
