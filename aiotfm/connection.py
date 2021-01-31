import asyncio
import logging
from asyncio import AbstractEventLoop, Protocol, BaseTransport, Transport
from typing import Optional, Tuple

import aiotfm  # circular import, don't `import from`
from aiotfm.errors import AiotfmException

logger = logging.getLogger('aiotfm')


class TFMProtocol(Protocol):
	def __init__(self, conn):
		self.buffer: bytearray = bytearray()
		self.client: aiotfm.Client = conn.client
		self.connection: Connection = conn
		self.length: int = 0

	def data_received(self, data: bytes):
		self.buffer.extend(data)

		while len(self.buffer) > self.length:
			if self.length == 0:
				for i in range(5):
					byte = self.buffer.pop(0)
					self.length |= (byte & 127) << (i * 7)

					if not byte & 0x80:
						break
				else:
					raise Exception("wtf") # pragma: no cover

			if len(self.buffer) >= self.length:
				self.client.data_received(self.buffer[:self.length], self.connection)
				del self.buffer[:self.length]
				self.length = 0

	def connection_made(self, transport: BaseTransport):
		# :desc: Called when a connection has been successfully made with the server.
		# :param connection: :class:`Connection` the connection that has been made.
		self.connection.open = True
		self.client.dispatch('connection_made', self.connection)

	def connection_lost(self, exc: Optional[Exception] = None):
		self.connection.open = False

		if exc is None:
			logger.info('Connection %s has been lost.', self.connection.name)
		else:
			logger.error('Connection %s has been lost. Reason:', self.connection.name, exc_info=exc)
			# :desc: Called when a connection has been lost due to an error.
			# :param connection: :class:`Connection` the connection that has been lost.
			# :param exception: :class:`Exception` the error which occurred.
			self.client.dispatch('connection_error', self.connection, exc)

		if self.connection.name == "main" and not self.client._close_event.done():
			self.client._close_event.set_result(('connection_lost', 10, None))


class Connection:
	"""Represents the connection between the client and the host."""
	PROTOCOL = TFMProtocol

	def __init__(self, name: str, client: 'aiotfm.Client', loop: AbstractEventLoop):
		self.name: str = name
		self.client: aiotfm.Client = client
		self.loop: AbstractEventLoop = loop

		self.address: Tuple[str, int] = None
		self.protocol: Protocol = None
		self.transport: Transport = None

		self.fingerprint: int = 0
		self.open: bool = False

	def __bool__(self):
		return self.open

	def _factory(self):
		return Connection.PROTOCOL(self)

	async def connect(self, host: str, port: int):
		"""|coro|
		Connect the client to the host:port
		"""
		self.address = (host, port)
		self.transport, self.protocol = await asyncio.wait_for(self.loop.create_connection(self._factory, host, port), 3)

	async def send(self, packet: 'aiotfm.Packet', cipher: bool = False):
		"""|coro|
		Send a packet to the socket

		:param packet: :class:`aiotfm.Packet` the packet to send.
		:param cipher: :class:`bool` whether or not the packet should be ciphered before sending it.
		"""
		if not self.open:
			raise AiotfmException('Cannot send a packet to a closed Connection.')

		if not self.client.bot_role and cipher:
			packet.xor_cipher(self.client.keys.msg, self.fingerprint)

		self.transport.write(packet.export(self.fingerprint))
		self.fingerprint = (self.fingerprint + 1) % 100

	def close(self):
		"""Closes the connection."""
		self.open = False
		if self.transport is not None and not self.transport.is_closing():
			self.transport.write_eof()
			self.transport.close()

	def abort(self):
		"""Abort the connection."""
		self.transport.abort()
		self.close()
