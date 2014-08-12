Security
========

User data should not be sniffable
-----

Users of your service should be protected by high-grade transport security (TLS/SSL).
Your service should get at least an A on `Qualys SSL Test <https://www.ssllabs.com/ssltest/>`_, and all access to your API should be over TLS.


User-set secrets should not be recoverable
---------

User passwords should never be stored in plain text.
Use PBKDF2, bcrypt, or scrypt to protect them, as users may reuse username/password combinations

API keys should also not be recoverable through your interface -- encourage your users to connect to your service using a new key for each device.
Since they are random, in the case of a data breach, all API keys can be purged and recreated.

If your API service is for an application, make your app create an API key upon authentication, and use that for authenticating to the service.
This prevents having to store user secrets on the device, and allows your users to revoke access from old devices.
