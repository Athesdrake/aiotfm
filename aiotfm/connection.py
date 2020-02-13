import asyncio
import struct

from aiotfm.errors import InvalidSocketData


class TFMProtocol(asyncio.Protocol):
	def __init__(self, conn):
		self.buffer = bytearray()
		self.client = conn.client
		self.connection = conn

	def connection_made(self, transport):
		self.connection.open = True
		self.client.dispatch('connection_made', self.connection)

	def data_received(self, data):
		self.buffer.extend(data)

		while len(self.buffer) > 3:
			lensize = self.buffer[0]
			if lensize == 1:
				length = self.buffer[1]
			elif lensize == 2:
				length = struct.unpack('>H', self.buffer[1:3])[0]
			elif lensize == 3:
				length = int.from_bytes(self.buffer[1:4], 'big')
			else:
				self.connection.abort()
				self.connection_lost(InvalidSocketData(
					f'The connection {self.connection.name} received a non-valid type of '
					f'{lensize} bytes.'
				))

			start = lensize + 1
			stop = start + length
			if len(self.buffer) < stop:
				break

			self.client.data_received(self.buffer[start:stop], self.connection)
			del self.buffer[:stop]

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
				self.client.create_task(self.client.restart_soon())
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