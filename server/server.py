#!/usr/bin/env python
print "boot"
import os; os.chdir(os.path.dirname(__file__))
import sys

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class Echo(Protocol):
    def connectionMade(self):
        self.transport.write("Hello client, I am the server!\n")
        reactor.callLater(3, self.transport.loseConnection)

    def dataReceived(self, data):
        sys.stdout.write(data)

def main():
    print "main"
    endpoint = TCP4ServerEndpoint(reactor, 8007)
    endpoint.listen(Factory.forProtocol(Echo))
    print "running reactor"
    reactor.run()
    

if __name__ == "__main__":
    main()
