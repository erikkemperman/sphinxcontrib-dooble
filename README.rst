====================
sphinxcontrib-dooble
====================

.. image:: https://img.shields.io/pypi/v/sphinxcontrib-dooble.svg
        :target: https://pypi.python.org/pypi/sphinxcontrib-dooble

.. image:: https://travis-ci.org/MainRo/sphinxcontrib-dooble.svg?branch=master
    :target: https://travis-ci.org/MainRo/sphinxcontrib-dooble

A sphinx extension for dooble.

Installation
------------

.. code:: console

    pip install dooble

Usage
------

In your sphinx project configuration, add dooble to the extensions:

.. code:: python

    extensions = [
        'sphinxcontrib_dooble',
    ]

Then marble diagrams can be added with the new *marble* directive:

.. code::

    .. marble::
        :alt: map

        ---1---2---3---4--->
        [   map(i: i*2)    ]
        ---2---4---6---8--->


