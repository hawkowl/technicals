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


How does the Linode DNSManager API achieve this?
------------------------------------------------

The DNSManager API is a `single endpoint API <layout.html#Single Endpoint API>`_

