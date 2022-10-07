arm64 plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This is a simple plugin that makes it as easy as possible to get started using
Tutor on ARM64 systems.

Installation
------------

::

    pip install git+https://github.com/open-craft/tutor-contrib-arm64

Usage
-----

::

    tutor plugins enable arm64
    tutor local quickstart

Images Used
-----------

Note: this plugin uses `unofficial Tutor images <https://hub.docker.com/r/opencraft/openedx-arm64/tags>`_ instead of the
latest, official docker images from Tutor. These images should be identical to the official ones other than being built
for ARM64; however, they are not updated as frequently.


Publishing new images to Docker Hub
-----------------------------------

Users of this plugin should not need to do this; this is more a "note to self" for this plugin's maintainer.

To build and publish new images::

    git checkout nightly
    git pull
    tutor images build openedx --no-cache
    tutor images build permissions --no-cache
    tutor images push openedx
    tutor images push permissions

Then ``git checkout master`` and run the same commands again.

License
-------

This software is licensed under the terms of the AGPLv3.
