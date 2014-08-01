Versioning
==========

Explicit versioning helps keep APIs stable
-------

When updating or changing your API, you need to make sure that existing users are still able to use your service.
Updates that change functionality, remove features, or otherwise alter the 'API contract' may have a knock-on effect and cause API clients to stop working.

By explicitly versioning your API, you can declare that the changes constitute a new 'API contract', but keep the existing interface operating until users have updated.

Documentation should aid client updating
------

By detailing the differences between one version and the next, upgrading is made far simpler for the implementors.

**Tenet:**
Good APIs have versions.

**Tenet:**
Good URIs never change, so your version should be explicitly in the URI.

**Tenet:**
Utilising API URIs that don't specify a version will eventually cause unmaintained applications to break.

**Tenet:**
Good APIs should document what has changed between versions.


