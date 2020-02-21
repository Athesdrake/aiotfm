import asyncio


class TFMProtocol(asyncio.Protocol):
	def __init__(self, conn):
		self.buffer = bytearray()
		self.client = conn.client
		self.connection = conn
		self.buffer_length = 0
		self.length_bytes = 0
		self.length = 0
		self.read_length = False

	def connection_made(self, transport):
		self.connection.open = True
		self.client.dispatch('connection_made', self.connection)

	def data_received(self, data):
		self.buffer_length += len(data)
		self.buffer.extend(data)

		while self.buffer_length > 0:
			while self.buffer_length > 0 and not self.read_length:
				self.buffer_length -= 1
				byte = self.buffer.pop(0)
				self.length |= (byte & 127) << (self.length_bytes * 7)
				self.length_bytes += 1

				if byte & 128 == 128 and self.length_bytes < 5:
					continue

				self.read_length = True

			if self.read_length and self.buffer_length >= self.length:
				self.client.data_received(self.buffer[:self.length], self.connection)
				del self.buffer[:self.length]
				self.buffer_length -= self.length

				self.length_bytes = 0
				self.length = 0
				self.read_length = False

			else:
				break

	def connection_lost(self, exc):
		self.connection.open = False

		if exc is not None:
			future = self.client.dispatch('connection_error', self.connection, exc)
			if future is not None:
				# This future is a wrapper for _run_event, which returns True if the event
				# ran successfully, False otherwise.
				# If it returns False, it already handled the auto_restart.
				if not asyncio.ensure_future(future):
					return

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