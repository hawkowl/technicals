Sending Mail
============

Sometimes, your application may want to send an email.
Below is a function which you can use to send mail over an encrypted connection and authenticating to the server:

:download:`esmtpmail.py`

.. literalinclude:: esmtpmail.py

How can it be encrypted if the reactor connects over TCP, and not SSL/TLS?
Not to worry -- ESMTP implements ``STARTTLS`` (you can find more details on it `here <http://en.wikipedia.org/wiki/STARTTLS>`_.
This 'upgrades' the connection from cleartext to an encrypted one before any sensitive data is sent.

The implementation of ``ESMTPSenderFactory``, which this code uses, requires the use of encryption (see ``ESMTPSender``'s `source <http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.2.0/twisted/mail/smtp.py#L1869>`_).

Here is an example, using the above:

:download:`email_example.py`

.. literalinclude:: email_example.py

Upon running it, you will get something like this:

.. code-block:: sh

    $ python email_example.py
    (1, [('hawkowl@atleastfornow.net', 250, '2.1.5 Ok')])

This is the result returned by the ``sendMail`` function, and will let you know what the status of the email is.
It is a 2-tuple containing how many addresses the mail was sent successfully to (1, if you're only sending to the one address), and a list of the results per address sent to -- which is, itself, a 3-tuple containing the email, the status code, and the textual representation (in the example, the response of 250 says that everything is OK).