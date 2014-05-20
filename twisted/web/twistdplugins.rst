Using the Twisted Web ``twistd`` Plugin
=======================================

Twisted provides a plugin for the ``twistd`` application runner, out of the box.
It can be run by running ``twistd web`` from the command line.

Setting the Port
----------------

To set the port that ``twistd web`` will listen on, specify the ``--port`` argument to ``twistd web`` with an endpoint description string understandable by :api:`twisted.internet.endpoints.serverFromString <serverFromString>` .
For example, ``--port tcp:8080`` will make it listen on TCP port 8080.

Serving Static Files
--------------------

To serve static files, specify the ``--path`` argument to ``twistd web`` to spec
