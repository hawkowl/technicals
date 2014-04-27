from __future__ import print_function
from esmtpmail import sendMail # the code above
from email import message
from twisted.internet.task import react

def main(reactor):

    m = message.Message()
    m.add_header("To", "hawkowl@atleastfornow.net")
    m.add_header("From", "hawkowl@atleastfornow.net")
    d = sendMail("hawkowl@atleastfornow.net", "password",
                 "mail.atleastfornow.net", 587, m)
    d.addCallback(print)
    return d

react(main)