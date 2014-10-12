#!/usr/bin/env python
print "boot"
import os; os.chdir(os.path.dirname(__file__))
import sys

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import SSL4ServerEndpoint
from twisted.internet import ssl
from twisted.internet import reactor
from twisted.python import log

class Echo(Protocol):
    def connectionMade(self):
        self.transport.write("Hello client, I am the server!\n")
        reactor.callLater(3, self.transport.loseConnection)

    def connectionLost(self, derp):
        print "connection lost"

    def dataReceived(self, data):
        sys.stdout.write(data)


def get_endpoint():
    serv = sys.argv[1]
    ca = sys.argv[2]
    print "using server identification", serv
    servdata = (
            open("./" + serv + ".crt.pem", "r").read()
          + open("./" + serv + ".key.pem", "r").read()
    )
    cadata = open("../" + ca + ".crt.pem", "r").read()
    cert = ssl.PrivateCertificate.loadPEM(servdata)
    authority = ssl.Certificate.loadPEM(cadata)
    endpoint = SSL4ServerEndpoint(reactor,
            8006, cert.options(authority))
    return endpoint


def main():
    log.startLogging(sys.stdout)
    print "main"

    endpoint = get_endpoint()

    endpoint.listen(Factory.forProtocol(Echo))
    print "running reactor"
    reactor.run()
    

if __name__ == "__main__":
    main()
