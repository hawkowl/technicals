Layout
======

Single Endpoint API
-------------------

An API where everything is on a single endpoint.
Query arguments are then added to this endpoint, with one or more of them indicating what function should be run, and one or more indicating what data or identifier to operate on.

Real World Example: Linode
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Linode API <https://www.linode.com/api>`_ uses this structure.
Their base API endpoint is located at``https://api.linode.com/``, and everything is run from this root.

An example of an API request that runs the ``test.echo`` function with the API key ``sekrit`` is:

.. code-block:: sh

    $ curl "https://api.linode.com/?api_key=sekrit&api_action=test.echo&foo=bar"


Function Endpoint API
---------------------

An API where there are multiple endpoints, each providing a function to run. 
Query arguments are then added to these endpoints, which specify what data or identifier to operate on.

Example: Blog
~~~~~~~~~~~~~

Imagine a blog which uses this structure.
They have an endpoint for creating blog posts at ``https://blog.example.com/api/create_post``, and an endpoint to delete a post at ``https://blog.example.com/api/delete_post``.

To create a post, this API request may be used:

.. code-block:: sh

    $ curl "https://blog.example.com/api/create_post?title=test&content=test

This would create a blog post on this service, and somehow return some kind of ID for the new post.
To delete it, they would then use this request:

.. code-block:: sh

    $ curl "https://blog.example.com/api/delete_post?id=1"


RFC-3986 Style API
------------------

An API which is laid out in the vein of :rfc:`3986`.
This is characterised by object types and identifiers being in the URI.

Examples of URIs:

* ``https://api.stripe.com/v1/charges/{CHARGE_ID}`` (`Stripe API <https://stripe.com/docs/api>`_, with URI versioning, see :doc:`versioning`)
