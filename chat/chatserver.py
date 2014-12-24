from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory

class MyChat(basic.LineReciever):
    def connectionMade(self):
        print "Got new Client! lulz!"
        self.transport.write('connected...\n')
        self.factory.clients.append(self)
        
    def connectionLost(self, reason):
        print "Lost a Client!"
        self.factory.clients.remove(self)
        
    def dataRecieved(self, data):
        print "recieved", repr(data)
        for c in self.factory.clients:
            c.message(data)
            
    def message(self, message):
        self.transport.write(message + '\n')
        
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import protocol
from twisted.application import service, internet

from twisted.internet.protocol import Factory
class ChatFactory(Factory):
    protocol = MyChat
    clients = []

    resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
    root = Resource()
    #serve chat protocol on /ws
    root.putChild("ws",resource)

    application = service.Application("chatserver")
    #run a TCP server on port 1025, serving the chat protocol.
    internet.TCPServer(1025, Site(root)).setServiceParent(application)