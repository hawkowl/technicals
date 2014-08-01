Pragmatic REST
============

There is a lot of debate about what "REST" is, and what makes a REST-ful API.
Arguments such as what the ``POST``, ``PUT``, and ``PATCH`` methods `should <https://news.ycombinator.com/item?id=7961944>`_ `do <https://news.ycombinator.com/item?id=5219444>`_ and whether function endpoints are RESTful.

My opinion on all this is that REST, like all other design patterns, is only useful as long as it is pragmatic.

What is REST in the first place?
---------

REST  -- meaning Representational State Transfer -- is when state transforms (such as 'create', 'update', or 'delete') or other idempotent operations (such as 'read') are mapped to the standard HTTP methods.

This makes it very useful in CRUD systems ("Create, Read, Update, Delete", the common life cycle of a general data object).


Method in the madness
------------

If you read :rfc:`7231`, the HTTP/1.1 Semantics RFC (which obsoletes :rfc:`2616`, the original HTTP/1.1 RFC), it says that:

     The GET method requests transfer of a current selected representation for the target resource.

     The POST method requests that the target resource process the representation enclosed in the request according to the resource's own specific semantics.

     The PUT method requests that the state of the target resource be created or replaced with the state defined by the representation enclosed in the request message payload.

     The DELETE method requests that the origin server remove the association between the target resource and its current functionality.

:rfc:`5789` further extends :rfc:`7231`/:rfc:`2616` and says:

    The PATCH method requests that a set of changes described in the request entity be applied to the resource identified by the Request-URI.

In the context of a CRUD system, this means:

* ``PUT`` is used when the resource's ID is known.
  ``POST`` can be used to create by sending the desired new data to a 'list resource', which will return the information required.
* ``GET`` reads.
* ``PUT`` updates in entirety and ``PATCH`` updates portions.
  ``POST`` can be used to do either, and is defined by the resource.
* ``DELETE`` does what it says on the tin.


As long as it makes sense, don't let this bind you
----

The best thing for any service to do is act according to the **principal of least surprise**.
That is, provided a list of endpoints, what different HTTP methods do should be obvious, or make sense with minimal effort.
Following the REST paradigm to the letter can help fulfill this principal of least surprise for those people that know it, but systems can use less methods where it makes sense, or such fine-grained control will not be required.




