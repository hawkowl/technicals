Sending Mail
============

Sometimes, your application may want to send an email.
Below is a function which you can use to send mail over an encrypted connection and authenticating to the server:

:download:`esmtpmail.py`

.. literalinclude:: esmtpmail.py

How can it be encrypted if the reactor connects over TCP, and not SSL/TLS?
Not to worry -- ESMTP implements ``STARTTLS`` (you can find more details on it `here <http://en.wikipedia.org/wiki/STARTTLS>`_).
This 'upgrades' the connection from cleartext to an encrypted one before any sensitive data is sent.

The implementation of ``ESMTPSenderFactory``, which this code uses, requires the use of encryption (see ``ESMTPSender``'s `source <http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.2.0/twisted/mail/smtp.py#L1869>`_).

Here is an example, using the above:

:download:`email_example.py`

.. literalinclude:: email_example.py

Upon running it, you will get something like this:

.. code-block:: sh

    $ python email_example.py
    (1, [('hawkowl@atleastfornow.net', 250, '2.1.5 Ok')])

The printed line is the result of the Deferred that is returned by ``sendMail``, once the mail transaction has been completed.

The result is a 2-tuple containing how many addresses the mail was sent successfully to and the sending results.
The sending results is a list of 3-tuples containing the email, the SMTP status code (see section 4.2 of `the RFC <http://www.ietf.org/rfc/rfc2821.txt>`_), and the dot-separated `ESMTP status code <https://www.iana.org/assignments/smtp-enhanced-status-codes/smtp-enhanced-status-codes.xhtml>`_, for each recepient.
In the example, the SMTP code of 250 says that everything is OK, and the ESMTP status "2.1.5 Ok" means that the recepient address was valid.
