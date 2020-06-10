import asyncio


class TFMProtocol(asyncio.Protocol):
	def __init__(self, conn):
		self.buffer = bytearray()
		self.client = conn.client
		self.connection = conn
		self.length = 0

	def data_received(self, data):
		self.buffer.extend(data)

		while len(self.buffer) > self.length:
			if self.length == 0:
				for i in range(5):
					byte = self.buffer.pop(0)
					self.length |= (byte & 127) << (i * 7)

					if not byte & 0x80:
						break
				else:
					raise Exception("wtf")

			if len(self.buffer) >= self.length:
				self.client.data_received(self.buffer[:self.length], self.connection)
				del self.buffer[:self.length]
				self.length = 0

	def connection_made(self, transport):
		# :desc: Called when a connection has been successfully made with the server.
		# :param connection: :class:`Connection` the connection that has been made.
		self.connection.open = True
		self.client.dispatch('connection_made', self.connection)

	def connection_lost(self, exc):
		self.connection.open = False

		if exc is not None:
			# :desc: Called when a connection has been lost due to an error.
			# :param connection: :class:`Connection` the connection that has been lost.
			# :param exception: :class:`Exception` the error which occurred.
			self.client.dispatch('connection_error', self.connection, exc)

		if self.connection.name == "main":
			if self.client.auto_restart:
				self.client.loop.create_task(self.client.restart_soon())
			else:
				self.client.close()


class Connection:
	"""Represents the connection between the client and the host."""
	PROTOCOL = TFMProtocol

	def __init__(self, name, client, loop):
		self.name = name
		self.client = client
		self.loop = loop

		self.address = None
		self.protocol = None
		self.transport = None

		self.fingerprint = 0
		self.open = False

	def _factory(self):
		return Connection.PROTOCOL(self)

	async def connect(self, host, port):
		"""|coro|
		Connect the client to the host:port
		"""
		self.address = (host, port)
		self.transport, self.protocol = await self.loop.create_connection(self._factory, host, port)

	async def send(self, packet, cipher=False):
		"""|coro|
		Send a packet to the socket

		:param packet: :class:`aiotfm.Packet` the packet to send.
		:param cipher: :class:`bool` whether or not the packet should be ciphered before sending it.
		"""
		if not self.open:
			return

		if cipher:
			packet.xor_cipher(self.client.keys.msg, self.fingerprint)

		self.transport.write(packet.export(self.fingerprint))
		self.fingerprint = (self.fingerprint + 1) % 100

	def close(self):
		"""Closes the connection."""
		self.open = False
		if not self.transport.is_closing():
			self.transport.write_eof()
			self.transport.close()

	def abort(self):
		"""Abort the connection."""
		self.transport.abort()
		self.close()
