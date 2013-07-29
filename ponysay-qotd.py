#!/usr/bin/env python3
import random
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import ponysay

# Quote-Of-The-Day protocol implementation using ponysay backend
# See RFC865 ( https://tools.ietf.org/html/rfc865 ) for details.
# To prevent traffic amplification attacks we are only providing a TCP service.

class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass

ponylist = ponysay.list_ponies_with_quotes()

class QOTDHandler(BaseRequestHandler):
	def handle(self):
		pony = random.choice(ponylist)
		s = ponysay.render_pony(pony, ponysay.random_quote(pony),
			balloonstyle=ponysay.balloonstyles['cowsay'],
			center=True,
			centertext=False)
		self.request.sendall(bytes(s, "UTF-8"))

if __name__ == "__main__":
	HOST, PORT = "", 8017
	server = ThreadingTCPServer((HOST, PORT), QOTDHandler)
	server.serve_forever()
