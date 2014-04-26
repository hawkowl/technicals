Sending Mail
============

Here's a function to send some email, over TLS.

    def sendMail(authUsername, authPassword, SMTPHost, SMTPPort, fromEmail, msg):

        contextFactory = ClientContextFactory()
        contextFactory.method = SSLv3_METHOD

        resultDeferred = Deferred()

        msgstring = msg.as_string(unixfrom=True)
        fp = StringIO(msgstring)

        senderFactory = ESMTPSenderFactory(
            authUsername, authPassword, fromEmail, msg.get("To"), fp,
            resultDeferred, contextFactory=contextFactory)
        senderFactory.noisy = False

        reactor.connectTCP(SMTPHost, SMTPPort, senderFactory)

        return resultDeferred
