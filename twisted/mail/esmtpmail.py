from cStringIO import StringIO
from twisted.internet import reactor, endpoints, defer
from twisted.mail.smtp import ESMTPSenderFactory

def sendMail(username, password, host, port, msg):
    """
    Send an email message using authenticated and encrypted SMTP.

    @param username: Username to use.
    @param password: Password to use.
    @param host: SMTP server's hostname or IP address.
    @param port: The port to connect to for SMTP.
    @param msg: Email to send.
    @type msg: L{email.message.Message}

    @return: A L{Deferred} that fires with the result of the email being
             sent.
    """
    resultDeferred = defer.Deferred()

    fp = StringIO(msg.as_string(unixfrom=True))

    senderFactory = ESMTPSenderFactory(username, password, msg.get("From"),
        msg.get("To"), fp, resultDeferred)

    endpoints.HostnameEndpoint(reactor, host, port).connect(senderFactory)

    return resultDeferred
