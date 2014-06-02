Deconstructing the Linode DNSManager API
========================================

Linode provides a service to their customers called `DNS Manager <https://library.linode.com/dns-manager>`_.
This allows you to create and modify name server records to be served from Linode's DNS infrastructure, without having to maintain your own name server.

Deconstructing, analysing and reconstructing this API is the topic of this Technical.


What does this API achieve?
---------------------------

As mentioned above, this API allows users to create and modify name server records.
To achieve this, you should be able to do the following things:

* List, create, update and delete master zones (domains)
* List, create, update and delete slave zones (which replicate from master zones)
* List, create, update and delete records under master zones

Records may also have a type (for example ``A``, the IPv4 record, or ``AAAA``, the IPv6 record), and types have differing requirements, so the data for each needs to be captured.


How does the API achieve this?
------------------------------

The DNSManager API is a Single Endpoint API (see :doc:`layout` for details) that is shared with Linode's other APIs.

You send it requests to its endpoint (``https://api.linode.com/``) with query arguments that specify the function you wish to run, along with some arguments that match the specific function.

Authentication is done by either providing an API key as the password in a HTTP BASIC Authorization header, or putting it in the ``api_key`` query argument.

Transport security is provided via TLS, with support for ECDHE (and therefore forward secrecy).

The response to each request is a JSON object, consisting of three keys:

* ``DATA`` -- the data of the response
* ``ACTION`` -- the action that was run
* ``ERRORARRAY`` -- an array of error messages, empty if successful.
  The errors are in therwise a list of dicts containing the keys ``ERRORCODE`` and ``ERRORMESSAGE``, which is the code


How is the API used?
--------------------

An API key is required to use the Linode API.
One can be got from their web interface, using the ``user.getapikey`` function.

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_action=user.getapikey" \
	  -d "username=hawkowl" \
	  -d "password=7yId7UoGhsnYh1k"

This will respond with something similar to the following:

.. code-block:: json

    {
       "ERRORARRAY": [],
       "ACTION": "user.getapikey",
       "DATA": {
          "USERNAME": "hawkowl",
	  "API_KEY": "SECRETKEY"
       }
    }

.. note::
   
   All instances of ``SECRET_KEY`` would be where a valid Linode API key would be.
   It's much too long to display inline (60+ characters).

Linode provides an "echo" function for testing, and looks like the following:

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=test.echo" \
	  -d "foo=bar"

The ``test.echo`` function simply responds with what it was given, so it will respond as such if successful:

.. code-block:: json

    {
       "ERRORARRAY": [],
       "ACTION": "test.echo",
       "DATA": {
          "foo": "bar"
       }
    }
