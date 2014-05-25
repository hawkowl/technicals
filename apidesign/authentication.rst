Authentication
==============

**Tenet:**
Good API services have good authentication options.

For APIs that authenticate directly, these options are HTTP BASIC (*only* to be used if the transport is secure) or HMAC.
HTTP Digest requires challenge-response, which in my opinion makes it less useful for REST APIs.

It goes without saying that your API should provide :doc:`security <security>` via TLS, to protect these creds.

**Tenet:**
Good API services don't use user credidentials directly.

If you use HTTP BASIC, do **not** use the user's creds -- generate an API key instead.
With an API key, you can:

    - track what API consumer accesses what,
    - revoke compromised creds without causing the user undue pain,
    - not leak the user's password (which has a high probability of being reused!) in case the transport becomes insecure,
    - and separate the user's interactive logon creds (eg. your website) with their un-interactive logon creds (eg. smartphone/desktop applications, external web services).


