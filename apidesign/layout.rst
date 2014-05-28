Layout
======

Being built on top of HTTP, all web APIs use URLs (Uniform Resource Locators) in some way.
There are three main patterns in URL layout, which I have termed **Single Endpoint**, **Function Endpoint**, and **RFC-3986 Style**.

Single Endpoint
---------------

A *Single Endpoint* API is where all access is done through a single endpoint -- that is, one URL -- no matter what you are doing with it.
Query arguments are then added to this endpoint, somehow indicating what function should be run and what data or identifier to operate on.

Real World Example: Linode
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Linode API <https://www.linode.com/api>`_ uses this structure.
Their base API endpoint is located at ``https://api.linode.com/``, and everything is run from this root.

An example of an API request that runs the ``test.echo`` function with the API key ``sekrit`` is:

.. code-block:: sh

    $ curl "https://api.linode.com/?api_key=sekrit&api_action=test.echo&foo=bar"


Function Endpoint
-----------------

An API where there are multiple endpoints, each providing a function to run. 
Query arguments are then added to these endpoints, specifying what data or identifier to operate on.

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
This is characterised by object types and identifiers being in the URI.

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
There is a ``PATCH`` verb which developers could implement for updating instead.

.. code-block:: sh

    $ curl https://api.stripe.com/v1/customers/cus_46X1iCm5JBayfU \
           -u sk_test_BQokikJOvBiI2HlWgH4olfQ2: \
	   -d "description=Customer for test@example.com"

Deleting a customer uses the ``DELETE`` verb:

.. code-block:: sh

    $ curl https://api.stripe.com/v1/customers/cus_46X1iCm5JBayfU \
           -u sk_test_BQokikJOvBiI2HlWgH4olfQ2: \
	   -X DELETE
.. note::

   Use of ``-X`` overrides the HTTP verb that cURL uses.

Good URIs Never Change
~~~~~~~~~~~~~~~~~~~~~~

The benefit of such a layout is that the reference to any particular object always stays the same.
There is no 'leaking through' of the framework or the functions in the implementation, since you are putting data at an object, not running a 'function'.
