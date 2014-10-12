#!/usr/bin/env python
print "boot"
import os; os.chdir(os.path.dirname(__file__))
import sys

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor

class Echo(Protocol):
    def connectionMade(self):
        self.transport.write("Hello server, I am the client!\n")
        reactor.callLater(3, self.transport.loseConnection)

    def dataReceived(self, data):
        sys.stdout.write(data)

def main():
    print "main"
    point = TCP4ClientEndpoint(reactor, "localhost", 8007)
    d = point.connect(Factory.forProtocol(Echo))
    print "running reactor"
    reactor.run()

if __name__ == "__main__":
    main()
