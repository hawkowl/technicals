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
  The errors are in therwise a list of dicts containing the keys ``ERRORCODE`` and ``ERRORMESSAGE``, which is the code and the human readable message respectively.


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

Linode provides an "echo" function for testing.

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=test.echo" \
	  -d "foo=bar"

Since ``test.echo`` function simply responds with what it was given, that request will respond with this on success:

.. code-block:: json

    {
       "ERRORARRAY": [],
       "ACTION": "test.echo",
       "DATA": {
          "foo": "bar"
       }
    }

If something goes wrong, it will respond with an error instead:

.. code-block:: json

     {
         "ERRORARRAY": [{
	     "ERRORCODE": 4,
	     "ERRORMESSAGE": "Authentication failed"
	 }],
	 "ACTION": "test.echo",
	 "DATA": {}
    }


Using the API in context
------------------------

To create a domain, we need to use the ``domain.create`` method.
This takes a `number of arguments <https://www.linode.com/api/dns/domain.create>`_, but a working command is below.

.. note::
   
   The API docs for Linode's ``domain.create`` method say that ``CustomerID`` is required.
   This is wrong.

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=domain.create" \
	  -d "Domain=mycoolawesomesite.net" \
	  -d "Type=master" \
	  -d "SOA_Email=hawkowl@atleastfornow.net"

.. code-block:: json

    {
        "ERRORARRAY": [],
	"ACTION": "domain.create"
	"DATA": {
	    "DomainID": 12345
	}
    }

``DomainID`` is what you want to hold onto.
This is the ID of your new domain, and you will need it to query it, delete it, or add entries to it.

We can query it like this:

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=domain.list" \
	  -d "DomainID=12345"

.. code-block:: json

    {
        "ERRORARRAY": [],
	"ACTION": "domain.list",
	"DATA": [{
            "DOMAINID": 12345,
            "DESCRIPTION": "",
            "EXPIRE_SEC": 0,
            "RETRY_SEC": 0,
            "STATUS": 1,
            "LPM_DISPLAYGROUP": "",
            "MASTER_IPS": "",
            "REFRESH_SEC": 0,
            "SOA_EMAIL": "hawkowl@atleastfornow.net",
            "TTL_SEC": 0,
            "DOMAIN": "mycoolawesomesite.net",
            "AXFR_IPS": "none",
            "TYPE": "master"
	}]	
    }

.. note::
   
   Not giving the ``DomainID`` key will make it return all domains under your account.

We can then add what Linode calls "resources" to this domain, such as subdomains.

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=domain.resource.create" \
	  -d "DomainID=12345" \
	  -d "Type=A" \
	  -d "Name=www" \
	  -d "Target=203.0.113.27"

.. code-block:: json

   {
        "ERRORARRAY": [],
	"ACTION": "domain.resource.create",
	"DATA": {
	    "ResourceID": 7654321
	}
   }

There are several kinds of types of resources -- ``A``, ``AAAA``, ``TXT``, ``MX``, ``SRV``, ``NS`` and ``CNAME``.
They all share the same resource creation function, and some of the meanings of the parameters are overloaded.
None of the parameters other than ``Type`` or the ``DomainID`` are marked as universally required in the documentation, requiring you to read the description to see if it applies to the type you are creating.

For instance, the Target parameter has the following docs:

.. epigraph::

   *When Type=MX the hostname. When Type=CNAME the target of the alias. When Type=TXT the value of the record. When Type=A or AAAA the token of '[remote_addr]' will be substituted with the IP address of the request.*

The full documentation for this function can be found `on Linode's site <https://www.linode.com/api/dns/domain.resource.create>`_.

Listing resources works more or less the same as ``domain.list``.
A ``DomainID`` is given to ``domain.resources.list``, with an optional ``ResourceID`` to display only a single resource.
Otherwise, all resources under that domain are given.

.. code-block:: sh

   $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=domain.resource.list" \
	  -d "DomainID=12345" 

.. code-block:: json

   {
      "ERRORARRAY": [],
      "ACTION": "domain.resource.list",
      "DATA": [{
	 "DOMAINID": 12345,
	 "PORT": 80,
	 "RESOURCEID": 7654321,
	 "NAME": "www",
	 "WEIGHT": 5,
	 "TTL_SEC": 0,
	 "TARGET": "203.0.113.27",
	 "PRIORITY": 10,
	 "PROTOCOL": "",
	 "TYPE": "A"
      }]
   }


Shortfalls of the API
---------------------

As I see it, the current Linode API has the following shortfalls:

* The single endpoint is shared between all Linode API services, and there is no easy or quick way to restrict an API key to only access the DNSManager API.
  The docs say that you can achieve this by creating users and restricting their permissions, but I've not researched this further.
* There is no versioning of the API.
* The function-based approach makes it more complex to use the API by splitting up the reference to the object you wish to access over a method name (eg. ``domain.resource.list``) and then a set of parameters, rather than having it directly in the URI.
* Creating domains and resources are more complex than required due to meanings of parameters being overloaded.
  The documentation isn't great at explaining what you exactly need, either.


Re-engineering the API
----------------------

Now that we have analysed how the API works and used it in context, I will now re-engineer it from the ground up, providing a proof in concept using the `Twisted asynchonous networking framework <https://twistedmatrix.com/trac/>`_ and the `Saratoga API development framework <https://github.com/hawkowl/saratoga>`_.

Layout
~~~~~~

The API will be in the RFC-3986 Style, with an explicit version in the path.
The whole API for this example will be dedicated to the DNSManager API.

Models
~~~~~~

The API needs to handle a few particular data models:

* Master Zones (which can have resources)
* Slave Zones (which can not have resources)
* Resources (individual records, under a zone)

I these can be better termed as **domains**, **zone mirrors**, and **records**, respectively.

Since we have two top level models, we should have them at the root:

.. code-block:: txt

   /domains
   /zonemirrors

You can then refer to individual domains and mirrors with an ID:

.. code-block:: txt

   /domains
   /domains/<ID>
   /zonemirrors
   /zonemirrors/<ID>

As domains can have records, we need to be able to refer to them too:

.. code-block:: txt

   /domains
   /domains/<ID>
   /domains/<ID>/records
   /domains/<ID>/records/<ID>
   /zonemirrors
   /zonemirrors/<ID>

But since different records have incredibly disparate data models depending on the type, it might be good to keep them seperate:

.. code-block:: txt

   /domains
   /domains/<ID>
   /domains/<ID>/A
   /domains/<ID>/A/<ID>
   /domains/<ID>/MX
   /domains/<ID>/MX/<ID>
   /domains/<ID>/NS
   /domains/<ID>/NS/<ID>
   /domains/<ID>/AAAA
   /domains/<ID>/AAAA/<ID>
   /domains/<ID>/TXT
   /domains/<ID>/TXT/<ID>
   /domains/<ID>/SRV
   /domains/<ID>/SRV/<ID>
   /domains/<ID>/CNAME
   /domains/<ID>/CNAME/<ID>
   /domains/<ID>/records
   /zonemirrors
   /zonemirrors/<ID>

This lets us get all of the records in one go, or all the records of a specific type.
Accessing a record individually has to be done through the correct type.
