Sending Mail
============

Sometimes, your application may want to send an email.
Below is a function which you can use to send mail over an encrypted connection and authenticating to the server:

:download:`esmtpmail.py`

.. literalinclude:: esmtpmail.py

How can it be encrypted if the reactor connects over TCP, and not SSL?
Not to worry - ESMTP implements ``STARTTLS``.
This 'upgrades' the connection from cleartext to an encrypted one before any data is sent.

The implementation of ``ESMTPSenderFactory``, which this code uses, requires the use of encryption for mail to be sent (see ``ESMTPSender``'s `source <http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.2.0/twisted/mail/smtp.py#L1869>`_).

Here is an example, using the above:

:download:`email_example.py`

.. literalinclude:: email_example.py

Upon running it, you will get something like this:

.. code-block:: sh

    $ python email_example.py
    (1, [('hawkowl@atleastfornow.net', 250, '2.1.5 Ok')])
