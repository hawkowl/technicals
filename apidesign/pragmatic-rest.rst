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

:rfc:`5789` further extends :rfc:`7231`/:rfc:`2616` and says:

    The PATCH method requests that a set of changes described in the request entity be applied to the resource identified by the Request-URI.

This basically can be summed up as:

* ``GET`` fetches the current state of the resource. 
* ``PUT`` replaces the current state of the resource, or creates it if it does not exist.
* ``PATCH`` replaces portions of the current state of the resource.
* ``POST`` gives a bundle of data to a resource, and it is completely up to the resource to decide what to do with it.

This means that 


