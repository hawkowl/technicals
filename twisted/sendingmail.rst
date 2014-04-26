Sending Mail
============

Sometimes, your application may want to send an email.
Below is a function which you can use to send mail over an encrypted connection and authenticating to the server::

    from cStringIO import StringIO
    from OpenSSL.SSL import SSLv3_METHOD
    from twisted.internet import reactor
    from twisted.internet.defer import Deferred
    from twisted.internet.ssl import ClientContextFactory
    from twisted.mail.smtp import ESMTPSenderFactory

    def sendMail(authUsername, authPassword, SMTPHost, SMTPPort, msg):
        """
        Send an email message using authenticated and encrypted SMTP.

        @param authUsername: Username to use.
        @param authPassword: Password to use.
        @param SMTPHost: SMTP server's hostname or IP address.
        @param SMTPPort: The port to connect to for SMTP.
        @param msg: Email to send.
        @type msg: L{email.Message}

        @return: A L{Deferred} that fires with the result of the email being
                 sent.
        """
        contextFactory = ClientContextFactory()
        contextFactory.method = SSLv3_METHOD

        resultDeferred = Deferred()

        msgstring = msg.as_string(unixfrom=True)
        fp = StringIO(msgstring)

        senderFactory = ESMTPSenderFactory(
            authUsername, authPassword, msg.get("From"), msg.get("To"), fp,
            resultDeferred, contextFactory=contextFactory)
        senderFactory.noisy = False

        reactor.connectTCP(SMTPHost, SMTPPort, senderFactory)

        return resultDeferred


Here is an example use of the above::

    from esmtpmail import sendMail
    from email import message
    from twisted.internet.task import react

    def main(reactor):

        m = message.Message()
        m.add_header("To", "hawkowl@atleastfornow.net")
        m.add_header("From", "hawkowl@atleastfornow.net")
        d = sendMail("hawkowl@atleastfornow.net", "password",
                     "mail.atleastfornow.net", 587, m)
        return d

    react(main)