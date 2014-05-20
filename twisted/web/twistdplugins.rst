Using the Twisted Web ``twistd`` Plugin
=======================================

Twisted provides a plugin for the ``twistd`` application runner, out of the box.
It can be run by running ``twistd web`` from the command line.

``twistd`` Options
------------------

``twistd`` has a few important global options -- the most useful of which is ``-n`` (or ``--nodaemon``).
This prevents ``twistd`` from forking to the background, and is handy for when you are testing or playing around with its functionality.

Setting the Port
----------------

To set the port that ``twistd web`` will listen on, specify the ``--port`` argument to ``twistd web`` with an endpoint description string understandable by :api:`twisted.internet.endpoints.serverFromString <serverFromString>` .
For example, ``--port tcp:8080`` will make it listen on TCP port 8080.


Serving Static Files
--------------------

To serve static files, specify the ``--path`` argument with the path that you wish to serve static files from.
As an example, ``twistd -n web --port tcp:8080 --path /tmp`` will serve your ``/tmp`` directory on port 8080.

Serving WSGI
------------

WSGI applications can be served by using the ``--wsgi`` argument with the fully qualified Python name of the WSGI application you wish to serve.

