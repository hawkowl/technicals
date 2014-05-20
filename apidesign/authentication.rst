Authentication
==============

**Tenet:**
Good APIs have good authentication options.

For APIs that authenticate directly, these options are HTTP BASIC (*only* to be used if the transport is secure) or HMAC.

**Tenet:**
Good APIs don't use user credidentials directly.

If you use HTTP BASIC, do **not** use the user's creds -- generate an API key instead.
With an API key, you can:

    - track what API consumer accesses what,
    - revoke compromised creds without causing the user undue pain,
    - not leak the user's password (which has a high probability of being reused!) in case the transport becomes insecure,
    - and separate the user's interactive logon creds (eg. your website) with their un-interactive logon creds (eg. smartphone/desktop applications, external web services).


