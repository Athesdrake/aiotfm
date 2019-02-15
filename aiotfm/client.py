import asyncio

from .packet import Packet
from .get_keys import get_keys
from .connection import Connection


class Client:
	LOG_UNHANDLED_PACKETS = False

	def __init__(self, loop=None):
		self.loop = loop or asyncio.get_event_loop()

		self.main = Connection('main', self, self.loop)
		self.bulle = None

		self.community = 0 # EN
		self.whisper_id = 0

	async def handle_packet(self, connection:Connection, packet:Packet):
		CCC = packet.readCode()
		if CCC==(26, 3): # Handshake ok
			online_players = packet.read32() # online players
			connection.fingerprint = packet.read8()
			community = packet.readString() # community
			country = packet.readString() # country
			self.authkey = packet.read32()

			self.loop.create_task(self._heartbeat_loop())

			await connection.send(Packet.new(8,2).write8(self.community).write8(0))

			os_info = Packet.new(28,17).writeString('en').writeString('Linux')
			os_info.writeString('LNX 29,0,0,140').write8(0)

			await connection.send(os_info)
			self.dispatch('login_ready', online_players, community, country)

		elif CCC==(5, 21): # Joined room
			private = packet.readBool()
			room_name = packet.readString() # Decode it at your own risk
			self.dispatch('joined_room', room_name, private)

		elif CCC==(16, 2): # Tribe invitation received
			author = packet.readUTF()
			tribe = packet.readUTF()
			self.dispatch('tribe_inv', author, tribe)

		elif CCC==(6, 6): # Room message
			player_id, username, commu, message = packet.unpack('LsBs')
			self.dispatch('room_message', username, message)

		elif CCC==(44, 1): # Bulle switching
			bulle_id = packet.read32()
			bulle_ip = packet.readString().decode()

			if self.bulle is not None:
				await self.bulle.close()

			self.bulle = Connection('bulle', self, self.loop)
			await self.bulle.connect(bulle_ip, self.main.address[1])
			await self.bulle.send(Packet.new(*CCC).write32(bulle_id))

		elif CCC==(44, 22): # Fingerprint offset changed
			connection.fingerprint = packet.read8()

		elif CCC==(60, 3): # Community platform
			TC = packet.read16()
			if TC==3: # Connected to the community platform
				self.dispatch('ready')
			elif TC==66: # Whisper
				author, commu, receiver, message = packet.readUTF(), packet.read32(), packet.readUTF(), packet.readUTF()
				self.dispatch('whisper', author, commu, receiver, message)
		else:
			if self.LOG_UNHANDLED_PACKETS:
				print(CCC, bytes(packet.buffer)[2:])

	async def receive_packet(self, packet, connection):
		self.dispatch('raw_socket', connection, packet.copy())
		await self.handle_packet(connection, packet)

	async def _heartbeat_loop(self):
		last_heartbeat = 0
		while self.main.open:
			if self.loop.time()-last_heartbeat>=10:
				await self.main.send(Packet.new(26, 26))
				if self.bulle is not None and self.bulle.open:
					await self.bulle.send(Packet.new(26, 26))

				last_heartbeat = self.loop.time()
			await asyncio.sleep(.5)

	async def start(self, api_tfmid, api_token):
		"""coro
		Starts the client."""

		self.keys = keys = await get_keys(api_tfmid, api_token)

		await self.main.connect('164.132.202.12', 5555)

		while not self.main.socket.connected:
			await asyncio.sleep(.1)

		packet = Packet.new(28, 1).write16(keys.version).writeString(keys.connection)
		packet.writeString('Desktop').writeString('-').write32(0x1fbd).writeString('')
		packet.writeString('74696720697320676f6e6e61206b696c6c206d7920626f742e20736f20736164')
		packet.writeString("A=t&SA=t&SV=t&EV=t&MP3=t&AE=t&VE=t&ACC=t&PR=t&SP=f&SB=f&DEB=f&V=LNX 29,0,0,140&M=Adobe Linux&R=1920x1080&COL=color&AR=1.0&OS=Linux&ARCH=x86&L=en&IME=t&PR32=t&PR64=t&LS=en-US&PT=Desktop&AVD=f&LFD=f&WD=f&TLS=t&ML=5.1&DP=72")
		packet.write32(0).write32(0x6257).writeString('')

		await self.main.send(packet)

	def event(self, coro):
		name = coro.__name__
		if not name.startswith('on_'):
			raise Exception("'{}' ins't a correct event naming.".format(name))
		if not asyncio.iscoroutinefunction(coro):
			raise Exception("Couldn't register a non-coroutine function for the event {}.".format(name))

		setattr(self, name, coro)
		return coro

	async def _run_event(self, coro, event_name, *args, **kwargs):
		try:
			await coro(*args, **kwargs)
		except asyncio.CancelledError:
			pass
		except Exception as e:
			if hasattr(self, 'on_error'):
				try:
					await self.on_error(event_name, e, *args, **kwargs)
				except asyncio.CancelledError:
					pass
				else:
					raise e
			else:
				raise e

	def dispatch(self, event, *args, **kwargs):
		method = 'on_' + event

		# add wait_for handling

		coro = getattr(self, method, None)
		if coro is not None:
			asyncio.ensure_future(self._run_event(coro, method, *args, **kwargs), loop=self.loop)

	async def login(self, username, password, room='1', encrypted=True):
		"""coro
		Log in the game."""

		if not encrypted:
			from .utils import shakikoo
			password = shakikoo(password)

		packet = Packet.new(26, 8).writeString(username).writeString(password)
		packet.writeString("app:/TransformiceAIR.swf/[[DYNAMIC]]/2/[[DYNAMIC]]/4")
		packet.writeString(room).write32(self.authkey^self.keys.auth)
		packet.cipher(self.keys.identification).write8(0)

		await self.main.send(packet)

	async def sendRoomMessage(self, message):
		"""coro
		Send a message to the room."""

		packet = Packet.new(6, 6).writeString(message)
		packet.xor_cipher(self.keys.msg, self.bulle.fingerprint)

		await self.bulle.send(packet)

	async def whisper(self, username, message):
		"""coro
		Whisper to a player."""

		self.whisper_id = (self.whisper_id + 1) % 0XFFFFFFFF

		packet = Packet.new(60, 3).write16(52).write32(self.whisper_id)
		packet.writeString(username).writeString(message)
		packet.xor_cipher(self.keys.msg, self.main.fingerprint)

		await self.main.send(packet)

	async def sendPrivateMessage(self, username, message):
		"""coro
		Deprecated alias for `Client.whisper`."""
		await self.whisper(username, message)

	async def playEmote(self, id, flag='be'):
		"""coro
		Play an emote id with it's optinnal flag (id = 10)."""

		packet = Packet.new(8, 1).write8(id).write32(0)
		if id==10:
			packet.writeString(flag)

		await self.bulle.send(packet)

	async def sendEmoticon(self, id):
		"""coro
		Send an emoticon to the server."""

		if 10>id>0:
			raise Exception('Invalid emoticon id')

		packet = Packet.new(8, 5).write8(id).write32(0)

		await self.bulle.send(packet)

	async def loadLua(self, lua_code):
		"""coro
		Load a lua code to the room."""

		if isinstance(lua_code, str):
			lua_code = lua_code.encode()

		packet = Packet.new(29, 1).write24(len(lua_code)).writeBytes(lua_code)

		await self.bulle.send(packet)

	async def sendCommand(self, cmd):
		"""coro
		Send a command to the game."""

		packet = Packet.new(6, 26).writeString(cmd)
		packet.xor_cipher(self.keys.msg, self.main.fingerprint)

		await self.main.send(packet)

	async def enterTribe(self):
		"""coro
		Enter the tribe house"""

		await self.main.send(Packet.new(16, 1))

	async def enterTribeHouse(self):
		"""coro
		Alias for Client.enterTribe"""

		await self.enterTribe()

	async def joinRoom(self, room_name):
		"""coro
		Join a room.
		The event 'on_joined_room' is dispatched when the client has successfully joined the room."""

		await self.main.send(Packet.new(5, 35).write8(255).writeString(room_name))

	async def enterInvTribeHouse(self, author):
		"""coro
		Join the tribe house of another player after receiving an /inv."""

		await self.main.send(Packet.new(16, 2).writeString(author))
