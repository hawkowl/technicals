Security
========

**Tenet:**
Good API services provide endpoints that employ high-grade transport layer security.

It is 2014, we don't need to be forcing our users to send data over RC4-(in)secured connections.
Your service should get at least an A on `Qualys SSL Test <https://www.ssllabs.com/ssltest/>`_.

**Tenet:**
Good API services should store no authentication-related information in plaintext.

User passwords should never be stored in plain text.
Use PBKDF2, bcrypt, or scrypt.
No exceptions.

API keys should also not be stored in plain text -- encourage your users to connect to your service using a new key for each device.

If your API service is for an application, make your app create an API key upon authentication, and use that for authenticating to the service instead.
