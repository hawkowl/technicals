==========================================
Using ``twistd`` to Start Your Application
==========================================

``twistd`` (pronounced "twist-dee") is an application runner for Twisted applications.
It takes care of starting your app, setting up loggers, daemonising, and providing a nice interface to start it.

Using the ``twistd web`` Plugin
===============================

Exposing a valid :api:`twisted.web.resource.IResource <IResource>` will allow your application to use the pre-existing ``twistd web`` plugin.

To enable this functionality, just expose the ``resource`` object of your Klein router:

.. literalinclude:: codeexamples/twistdPlugin.py

Then run it::

  twistd -n web --class=twistdPlugin.resource

The full selection of options you can give to ``twistd web`` can be found in its help page.
Here are some relevant entries in it:

.. literalinclude:: twistdwebman.txt

Using HTTPS via the ``twistd web`` Plugin
=========================================



things we should talk about here:

- set up klein in a class
- set up Options and makeService
- create a twisted tap file
- start it through twistd
- use https (FOR SECURITY)
