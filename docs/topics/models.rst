======================
Writing Models Plugins
======================

The model is the heart of Umbra. This is where the AI/ML routines are executed with all
of our carefully ingested and prepared datasets. The models allow for the datasets to
be used to train and build up the AI used to make predictions. The challenge is, as
always, to produce effective models.

The model though, does not need to be complex, it only needs to be able to take in training
and prediction data.

As always, Umbra is made using `pop` to create the plugin architecture. So you must accept
the `hub` as the first argument. The following arguments are `data` and `train`, these arguments
are the datasets used to predict and train. Here is how the setup looks:

.. code-block:: python


    from pyod.models.knn import KNN


    def __mod_init__(hub):
        hub.models.knn.COMPS = {}


    async def run(hub, pipe, data, train):
        '''
        Run the knn algorith on the given dataset
        '''
        if pipe not in hub.models.knn.COMPS:
            hub.models.knn.COMPS[pipe] = {'knn': KNN(contamination=0.01)}
        knn = hub.models.knn.COMPS[pipe]['knn']
        if train:
            knn.fit(train)
        if data:
            knn.fit(data)
            return knn.predict(data)
        return []

This is a great example of some of the benefits of `pop`. When the module is first loaded
we want to create a dict on the hub's namespace that we can use. The `__mod_init__` function
is executed just once, when the module is first loaded. This allows us to set up data on
the module's hub namespace. This is what you see when we set `hub.models.knn.COMPS`. This
allows us to persist things like the `knn` object that we are training.

As you can see, this is an extreamly simple example! Think of the model plugin interface as
just a doorway to hook into a larger model!