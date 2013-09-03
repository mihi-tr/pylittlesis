pylittlesis
===========

A python library wrapping the Little Sister API...

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
