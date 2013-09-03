pylittlesis
===========

`LittleSis`_ is a free database of who-knows-who in US Business and
Government. It provides an API to facilitate development of additional
plugins. This is a python wrapper to wrap the API into python objects.

.. _LittleSis: http://littlesis.org

installation
------------

Not on the cheeseshop yet so::

  pip install git+https://github.com/mihi-tr/pylittlesis.git

usage
-----

get entity 1::

  from littlesis import LittleSis
  ls=LittleSis(api_key)
  e=ls.entity(1)
  print e.details
