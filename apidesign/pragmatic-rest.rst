Pragmatic REST
============

There is a lot of debate about what "REST" is, and what makes a REST-ful API.
Arguments such as what the ``POST``, ``PUT``, and ``PATCH`` verbs `should <https://news.ycombinator.com/item?id=7961944>`_ `do <https://news.ycombinator.com/item?id=5219444>`_ and whether function endpoints are RESTful.

My opinion on all this is that REST, like all other design patterns, is only useful as long as it is pragmatic.

What ``POST``, ``PUT``, and ``PATCH`` should do
------------

If you read :rfc:`7231`, the HTTP/1.1 Semantics RFC (which obsoletes :rfc:`2616`), it says that:

     The GET method requests transfer of a current selected representation for the target resource.

     The POST method requests that the target resource process the representation enclosed in the request according to the resource's own specific semantics.

     The PUT method requests that the state of the target resource be created or replaced with the state defined by the representation enclosed in the request message payload.

     The DELETE method requests that the origin server remove the association between the target resource and its current functionality.

:rfc:`5789` further extends :rfc:`7231`/:rfc:`2616` and says:

    The PATCH method requests that a set of changes described in the request entity be applied to the resource identified by the Request-URI.

This basically can be summed up as:

* ``GET`` fetches the current state of the resource. 
* ``PUT`` replaces the current state of the resource, or creates it if it does not exist.
* ``PATCH`` replaces portions of the current state of the resource.
* ``POST`` gives a bundle of data to a resource, and it is completely up to the resource to decide what to do with it.
* ``DELETE`` destroys the current state of the resource.

This means that a system using only ``GET``, ``POST``, and ``DELETE`` can comply fully with :rfc:`7231` and perform all the required CRUD operations to be RESTful.


HTTP Verbs should do things that make *sense*
----

The best thing for any service to do is act according to the **principal of least surprise**.
That is, provided a list of endpoints, what different HTTP verbs do should be obvious, or make sense.

As an example, imagine a resource called ``cakes``:

* The most sensical thing for ``GET`` to do, with no query arguments, is list all resources under ``cakes`` with enough information to be useful (including the ID of each resource), without having to do subsequent requests.
* ``POST``\ ing to that endpoint should create a new resource under ``cakes``, and return the ID and a representation of the resource.
* ``cakes/<ID>`` should refer to an individual resource, and ``GET``\ tting it should return a representation of it.
* ``POST``\ ing to ``cakes/<ID>`` should update the resource using the parameters given.
  Replacing the entire object should involve defining every field to some new state.
* ``DELETE`` to ``cakes/<ID>`` should delete the resource, if it is allowed.
  Using this verb on ``cakes`` will do nothing, and should return ``405 Method Not Allowed``.

In this example, I only use ``GET``, ``POST``, and ``DELETE`` -- if users can decide their own IDs for resources, then ``PUT``\ ting to ``cakes/<ID>`` should create a new resource with that ID.



