===================
Understanding Flows
===================

The basic pattern used in AI/ML is Ingest -> Data Management -> AI/ML Model -> Output.
Umbra seeks to make these stages pluggable and re-usable through a system we call `flows`.

Flow Stages
===========

The `Flow` defines how this pipeline can be executed. Taking input data from any pluggable
source and then moving it through the process. Umbra breaks this process up into multiple
stages. These stages are called `ingress`, `data`, `model`, `egress`.

Ingress
-------

The ingress system is used to attach to an ongoing ingress system. Typically an event
based system. The event system will emit events as they occur and push them through the
pipeline. The ingress system can be a single instance ingress system as well, say in the
form of a json file.

Data
----

The data stage is used to create the input and output data paths. For most AI systems all
of the input data needs to be reduced to numbers. The data plugins are made to take arbitrary
data types and reform them into standardized data sets.

For instance the `salt_event` data plugin takes the information in the Salt event stream and
converts the words into numbers dynamically. The word datasets are created on the fly allowing
different matched event streams to be prepared.

Model
-----

The model is the meat of the process. This is the area where Umbra calls out to tools like
Tensorflow, pyod, and Scikit. The model receives the conditioned data from the data stage
and crunches it. The model will also determine if the data is to be used for training or
for predictions based on options like `train_for`.

Egress
------

Once the model has run it can emit predictions and suggestions. The Egress system allows for
the suggestions to be emitted out on another event based system. This can be an alerting system,
notifications, or just a datastore holding the information.

Flows and Pipes
===============

In the flow configurations you define pipes and each pipe has the options for the named stages,
as well as additional options for the pipe. All of the pipes defined in the flow files need to
have unique names.

A flow file with a single pipe called 'sh' looks like this:

.. code-block:: yaml

    sh:
      ingress:
        salt_event: 'salt/beacon/*/sh*'
      data: salt_event
      model: knn
      egress: salt_event
      train_for: 50000
      enabled: True

This defines that we will be attaching to the salt event bus as our ingress point and looking
for events that match the given tag. The data modifier to use is obviously `salt_event` because
we are attached to the salt_event ingress system. In this case we are using the simple `knn`
model for outlier detection. Finally the data will be emitted back on the `salt_event` system
as well.

The additional options here are `train_for` and `enabled`. The `train_for` option allows for
setting a finite number of data entries to train on before running predictions. `enabled`
allows you to enable or disable the given pipe.
