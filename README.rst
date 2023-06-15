arm64 plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin is deprecated:

🌴 **As of the Palm release of Open edX (June 14, 2023), and Tutor v16, ARM support and images are provided by Tutor!**

You can use Tutor 16+ out of the box on ARM systems without this plugin.




Introduction
------------

This is a simple plugin that makes it as easy as possible to get started using
Tutor v15 on ARM64 systems.

Supported Tutor versions: 15.3.3, 15.3.4, 15.3.5 and -nightly variants of each.

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

Note: this plugin uses
`unofficial Tutor images <https://github.com/open-craft/tutor-contrib-arm64/pkgs/container/openedx-arm64>`_ instead of
the latest, official docker images from Tutor. These images should be identical to the official ones other than being
built for ARM64; however, they are not updated as frequently.


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
