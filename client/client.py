#!/usr/bin/env python
print "boot"
import os; os.chdir(os.path.dirname(__file__))
import sys

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import SSL4ClientEndpoint
from twisted.internet import ssl
from twisted.internet import reactor
from twisted.python import log

class Echo(Protocol):
    def connectionMade(self):
        self.transport.write("Hello server, I am the client!\n")
        reactor.callLater(3, self.transport.loseConnection)

    def connectionLost(self, derp):
        print "connection lost"

    def dataReceived(self, data):
        sys.stdout.write(data)

def get_endpoint():
    client = sys.argv[1]
    ca = sys.argv[2]
    print "using client identification", client
    clientdata = (
            open("./" + client + ".crt.pem", "r").read()
          + open("./" + client + ".key.pem", "r").read()
    )
    cadata = open("../" + ca + ".crt.pem", "r").read()
    cert = ssl.PrivateCertificate.loadPEM(clientdata)
    authority = ssl.Certificate.loadPEM(cadata)
    return SSL4ClientEndpoint(reactor, "localhost", 8006,
            cert.options(authority))

def main():
    log.startLogging(sys.stdout)
    print "main"
    endpoint = get_endpoint()
    endpoint.connect(Factory.forProtocol(Echo))
    print "running reactor"
    reactor.run()

if __name__ == "__main__":
    main()
