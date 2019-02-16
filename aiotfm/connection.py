import asyncio

from .packet import Packet

class Socket:
	"""A socket class with asyncio."""
	def __init__(self, host, port, loop=None):
		self.loop = loop or asyncio.get_event_loop()

		self.__socket = asyncio.open_connection(host, port, loop=self.loop)
		self._reader:asyncio.StreamReader = None
		self._writer:asyncio.StreamWrite = None
		self.connected = False

	async def connect(self):
		"""|coro|
		Connect the socket to the host."""
		self._reader, self._writer = await self.__socket
		self.connected = True

		del self.__socket

	async def recv(self, size):
		"""|coro|
		Receive up to size bytes from the socket."""
		return await self._reader.read(size)

	async def send(self, data):
		"""|coro|
		Send a data string to the socket."""
		rval = self._writer.write(data)
		await self.flush()
		return rval

	async def flush(self):
		"""|coro|
		Flush send buffer."""
		await self._writer.drain()

	def close(self):
		"""Close the socket."""
		self.connected = False
		self._writer.close()

class Connection:
	"""Represents the connection between the client and the host."""
	def __init__(self, name, client, loop=None):
		self.name = name
		self.client = client
		self.loop = loop

		self.socket = None
		self.address = ()
		self.fingerprint = 0

		self.open = False

	async def connect(self, host, port):
		"""|coro|
		Connect the client to the host:port
		"""
		self.address = (host, port)
		self.socket = Socket(host, port, self.loop)

		await self.socket.connect()
		self.open = True

		self.client.dispatch('connection_made', self)

		asyncio.ensure_future(self._recv_loop())

	async def _recv_loop(self):
		"""|coro|
		The loop that receives data and send it to the Client.received_data method."""
		while self.open:
			lensize = await self.socket.recv(1)
			if len(lensize)==0:
				if self.open:
					raise EOFError('The connection "{.name}" has been closed.'.format(self))
				self.close()
				break
			length = int.from_bytes(await self.socket.recv(lensize[0]), 'big')
			data = await self.socket.recv(length)
			await self.client.received_data(data, self)

	async def send(self, packet):
		"""|coro|
		Send a packet to the socket
		"""
		await self.socket.send(packet.export(self.fingerprint))
		self.fingerprint = (self.fingerprint + 1) % 100

	def close(self):
		"""Closes the connection."""
		self.open = False
		self.socket.close()