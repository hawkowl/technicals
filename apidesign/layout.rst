Layout
======

Being built on top of HTTP, all web APIs use URLs (Uniform Resource Locators) in some way.
As the name suggests, they are a standard way of locating *resources*, which is a 'thing' which can accept or provide data.

There are three main patterns in URL layout, which I have termed **Single Endpoint**, **Function Endpoint**, and **RFC-3986 Style**.


Single Endpoint
---------------

A *Single Endpoint* API is where all access is performed by communication through a single endpoint -- that is, one URL -- no matter what you are doing with it.
Adding query arguments to requests to this endpoint then indicate what function should be run and what data to operate on.

Since a single endpoint is used, the whole service is a single 'resource'.
This is more akin to a remote procedure call interface than a REST-style web interface.


Real World Example: Linode
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Linode API <https://www.linode.com/api>`_ uses this structure, with their API endpoint at ``https://api.linode.com/``.

Using it involves  ``GET``/``POST`` requests to this URL, with an ``api_action`` query argument that denotes which 'function' to run.
Arguments to the function specified are then given by additional query arguments.

An example of an API request that runs the ``test.echo`` function with the API key ``SECRETKEY`` is:

.. code-block:: sh

    $ curl "https://api.linode.com/" \
          -d "api_key=SECRETKEY" \
          -d "api_action=test.echo" \
          -d "foo=bar"

You can see the full teardown and analysis of the DNS Manager portion of this API at :doc:`deconstructing-linode-dnsmanager`.


Function Endpoint
-----------------

An API where there are multiple endpoints, each providing a function to run. 
Query arguments are then added to these endpoints, specifying what data or identifier to operate on.

This layout is similar to **Single Endpoint**, but instead of specifying what function to run by a query argument, it is encoded in the URL.

Example: Blog
~~~~~~~~~~~~~

Imagine a blog which uses this structure.
They have an endpoint for creating blog posts at ``https://blog.example.com/api/create_post``, and an endpoint to delete a post at ``https://blog.example.com/api/delete_post``.

To create a post, this API request may be used:

.. code-block:: sh

    $ curl "https://blog.example.com/api/create_post?title=test&content=test"

This would create a blog post on this service, and somehow return some kind of ID for the new post.
To delete it, they would then use this request:

.. code-block:: sh

    $ curl "https://blog.example.com/api/delete_post?id=1"


RFC-3986 Style
--------------

An API which is laid out in the vein of :rfc:`3986`.
This is characterised by object types and identifiers being in the URL.

Laid out like this, it allows a single record of data to be referred to entirely in the URL.
Most uses of this style of API are data-driven -- when clients put information into the system, actions which handle new/changed data are run implicitly.
When 'functions' are required, they are usually handled by a resource that accepts ``POST`` requests.


Real World Example: Stripe
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Stripe API <https://stripe.com/docs/api>`_ uses this system.
Stripe is a payment processor, allowing companies to process credit card payments over the internet.

An example of this API is given in their docs, displayed here.
This example creates a new customer, using the API key ``sk_test_BQokikJOvBiI2HlWgH4olfQ2`` (with no password, as Stripe just use the one key), by ``POST`` ing at the ``customers`` object.

.. code-block:: sh

    $ curl "https://api.stripe.com/v1/customers" \
           -u sk_test_BQokikJOvBiI2HlWgH4olfQ2: \
	   -d "description=Customer for test@example.com" \
	   -d "card=tok_1046XL2eZvKYlo2CsaCAcF5P"

.. note::

   ``-d`` is the argument for adding HTTP ``POST`` data in cURL.
   The presence of ``-d`` changes the verb to ``POST`` implicitly.

The response then gives the identifier of the created customer.

The main difference between this style of API and the others is that accessing a customer is not done by giving a parameter (eg. in a query argument), but by adding the object type and identifier in the URI.
This example, also from the Stripe API docs, fetches a customer by ``GET`` ting a URI with the customer's identifier.

.. code-block:: sh

    $ curl "https://api.stripe.com/v1/customers/cus_46X1iCm5JBayfU" \
           -u sk_test_BQokikJOvBiI2HlWgH4olfQ2:

The URL is built as ``object/identifier`` -- customer ``1`` would be found at ``customers/1``, customer ``foo`` would be found at ``customers/foo``, and so on.

Performing actions on this particular customer becomes changing the HTTP verb from ``GET`` to the action you want.
Stripe's API uses ``POST`` for updating.

.. code-block:: sh

    $ curl https://api.stripe.com/v1/customers/cus_46X1iCm5JBayfU \
           -u sk_test_BQokikJOvBiI2HlWgH4olfQ2: \
	   -d "description=Customer for test@example.com"

.. note::

   There exists a ``PATCH`` verb which developers could implement for updating instead.

Deleting a customer uses the ``DELETE`` verb:

.. code-block:: sh

    $ curl https://api.stripe.com/v1/customers/cus_46X1iCm5JBayfU \
           -u sk_test_BQokikJOvBiI2HlWgH4olfQ2: \
	   -X DELETE
.. note::

   Use of ``-X`` overrides the HTTP verb that cURL uses.


Real World Example: Tesla Model S
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Tesla Model S' API <http://docs.timdorr.apiary.io/>`_ mostly follows this system, where vehicles are referred to by ID in the URI, but a request to a function endpoint under that vehicle will perform an action.

You can fetch resources as you expect:

.. code-block:: sh

   $ curl https://portal.vn.teslamotors.com/vehicles/1/command/gui_settings

.. code-block:: json

   {
      "gui_distance_units": "mi/hr",
      "gui_temperature_units": "F",
      "gui_charge_rate_units": "mi/hr",
      "gui_24_hour_time": false,
      "gui_range_display": "Rated"
   }

Running functions (which, in this case, does something in the real world!) is also possible by POST requests:

.. code-block:: sh

   $ curl -x POST https://portal.vn.teslamotors.com/vehicles/1/command/honk_horn

.. code-block:: json

   {
      "result": true,
      "reason": ""
   }


Resources, not functions
~~~~~~~~~~~~~~~~~~~~~~

The benefit of such a layout is that the reference to any particular object always stays the same.
There is no 'leaking through' of the framework or the implementation, since you are sending data to a resource, not running a 'function' to mutate/query it.
