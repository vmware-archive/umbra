=====================
Integrating with Salt
=====================

Umbra can integrate directly with a Salt Master to detect anomalies on the event bus. This
can be very useful when combined with a Salt Reactor. Use the following `flow` with umbra to
integrate with the `sh` beacon running on multiple minions:

.. code-block:: yaml

    sh:
      ingress:
        salt_event: 'salt/beacon/*/sh*'
      data: salt_event
      model: knn
      egress: salt_event
      train_for: 10000

This flow, saved to `/etc/umbra/flows/sh.yml` will now activate umbra to attach to the Salt
Master event bus, gather the events that match the given tag, and then emit events for strange
shell commands that are executed on the attached minions.

Now run `umbra` on the Salt Master, as the same user the Salt Master is running as. Umbra
will emit events onto the Salt Event Bus with the tag: `umbra/sh`. Now you can set up a
reactor to handle the events as the come in!

Please keep in mind that the `train_for` number might be too high, or too low based on your
environment.

Additional Beacons
==================

The goal of Umbra and Salt is to make extra use of the beacon system in Salt. Take a few moments
to review what beacons are currently in Salt, and consider what other beacons you could build that
will integrate with Umbra. Remember that adding beacons to Salt is very easy and Umbra is built to
automatically format and manage the data being sent back from beacons making it easy to
apply AI/ML to virtually any situation.
