.. templater documentation master file, created by
   sphinx-quickstart on Tue Jul 14 04:03:29 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to templater's documentation!
=====================================

Contents:

.. toctree::
   :hidden:

   Interface for easy input <tplinput>

About
=====
The templater bundle is an python software. It provides a command line program for creating files 
from templates. While creating the file the user is asked for input, specified in the template.

templater is built on top of `mako <www.makotemplates.org>` and `urwid <http://excess.org/urwid>` 
(only needed for curses interfaces input). 


Install
=======

You can install templater with::

    sudo python setup.py install

A script with name ``templater`` and an Python module ``tplinput`` will be installed. 
Additional a little start up with some template will be place under /usr/share/templater/.

Script Usage
============



For an startup call:

.. code-block:: bash

               templater -t TODO -o MyTODO

It will prompted for needed values and then create the file :file:`MyTODO`.
``-t`` specifies the template and ``-o`` the output file. If parameter ``-o`` is missing
then the output it printed to ``stdout``.

templater look in this directories:

#. :file:`$HOME/.templater/` 
#. :file:`$HOME/.templater/tpl.d`
#. :file:`/usr/templater/tpl.d`

It stop on the first found. 

Global/default values
=====================

.. highlighted:: python

You can define values, that you often use in your scripts at a central place.
The :file:`$HOME/.templater/defaults` it a python script. Every variable you define here is available in your templates. The default file is::


  # With this file you can set variables that you can use in your 
  # programms. You only need to define a variable in this context.
  # If you want to like a now variable you can do it!             
  #                                                               
  # In this file reigns python!                                   
  #                                                               
  # i.e.                                                          
  from datetime import datetime                                   
  now = datetime.now() 

Now you can use ``now`` directly as a variable in the template files. 
If you want the username in the available in every template you can append this to the file::

  from getpass import getuser
  username = getuser()

Writing my own templates
========================
The template language is mako, please refer to `mako documentation <www.makotemplates.org/doc>` 
for syntax of template language. 

Additional the templater software provids the ``tplinput`` module for an easy asking after values.
For example you can following snippet within an python code block to ask for projekt name, version and a long description::


  from tplinput  import cread, TextInput, Line, LongTextInput

  # ask for an curses ui, the values are return as a tuple
  # you can let python let it unpack: 

  name, version, desc = cread(
    Line('Enter values for the template script.sh'), #comment line
    TextInput('project name:'),   # single line input
    TextInput('Version:','1.0''), #   with an default value
    LongTextInput('Description:') # multiline input
  )


Look in the :mod:`tplinput` module for more :ref:`information <tplinput`.
