Versioning
==========

When updating or changing your API, you need to make sure that existing users are still able to use your service.
Updates that change functionality, remove features, or otherwise alter the 'API contract' may have a knock-on effect and cause API clients to stop working.
By explicitly versioning your API, you can declare that the changes constitute a new 'API contract', but keep the existing interface operating until users have updated.
Unmaintained or hard to update clients can be kept working with a subset of functionality of the new API, by just staying on the old version.

There are several ways of indicating that your API is versioned -- some services use a header to specify which version, and some put it directly in the URI.
I think that this is the best way of going about it, as it clearly namespaces your APIs, makes it directly obvious to the implementor what version they are using, and allows cleanup or alteration of the resource layout.

This versioning should occur as high up the tree as is possible, along product lines.
For example, a system that operates as one whole should be kept on the same version, but two different services of a company may be versioned different if each is accessed as a distinct different API.
