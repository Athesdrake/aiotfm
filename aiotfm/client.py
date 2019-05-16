import asyncio

from .packet import Packet
from .get_keys import get_keys
from .connection import Connection
from .player import Profile
from .tribe import Tribe


class Client:
	"""Represents a client that connects to Transformice.
	Two argument can be passed to the :class:`Client`.

	.. _event loop: https://docs.python.org/3/library/asyncio-eventloops.html

	Parameters
	----------
	community: Optional[:class:`int`]
		Defines the community of the client. Defaults to 0 (EN community).
	loop: Optional[event loop]
		The `event loop`_ to use for asynchronous operations. If ``None`` is passed (defaults),
		the event loop used will be ``asyncio.get_event_loop()``.
	"""
	LOG_UNHANDLED_PACKETS = False

	def __init__(self, community=0, loop=None):
		self.loop = loop or asyncio.get_event_loop()

		self.main = Connection('main', self, self.loop)
		self.bulle = None

		self._waiters = {}

		self.community = community # EN
		self.cp_fingerprint = 0

	async def received_data(self, data, connection):
		"""|coro|
		Dispatches the received data.

		:param data: :class:`bytes` the received data.
		:param connection: :class:`aiotfm.connection.Connection` the connection that received the data.
		"""
		self.dispatch('raw_socket', connection, Packet(data))
		await self.handle_packet(connection, Packet(data))

	async def handle_packet(self, connection:Connection, packet:Packet):
		"""|coro|
		Handles the known packets and dispatches events.
		Subclasses should handle only the unhandled packets from this method.

		Example: ::
			class SubClient(aiotfm.Client):
				async def handle_packet(self, conn, packet):
					tmp = packet.copy()
					handled = await super().handle_packet(conn, packet)
					packet = tmp

					if not handled:
						# Handle here the unhandled packets.
						pass

		:param connection: :class:`aiotfm.connection.Connection` the connection that received the packet.
		:param packet: :class:`aiotfm.Packet` the packet.
		:return: True if the packet got handled, False otherwise.
		"""
		CCC = packet.readCode()
		if CCC == (1, 1): # Old packets
			data = packet.readString().split(b'\x01')
			oldCCC = tuple(data.pop(0)[:2])
			self.dispatch('old_packet', connection, oldCCC, data)
			return await self.handle_old_packet(connection, oldCCC, data)

		elif CCC==(5, 21): # Joined room
			private = packet.readBool()
			room_name = packet.readString() # Decode it at your own risk
			self.dispatch('joined_room', room_name, private)

		elif CCC==(6, 6): # Room message
			player_id, username, commu, message = packet.unpack('LsBs')
			self.dispatch('room_message', username, message)

		elif CCC==(8, 16): # profile
			self.dispatch('profile', Profile(packet))

		elif CCC==(16, 2): # Tribe invitation received
			author = packet.readUTF()
			tribe = packet.readUTF()
			self.dispatch('tribe_inv', author, tribe)

		elif CCC==(26, 2): # Logged in successfully
			player_id = packet.read32()
			username = packet.readUTF()
			played_time = packet.read32()
			community = packet.read8()
			pid = packet.read32()
			self.dispatch('logged', player_id, username, played_time, community, pid)

		elif CCC==(26, 3): # Handshake OK
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

		elif CCC==(26, 12):
			self.dispatch('login_result', packet.read8(), packet.readUTF())

		elif CCC==(28, 6): # pong
			self.dispatch('ping', packet.read8())

		elif CCC==(44, 1): # Bulle switching
			bulle_id = packet.read32()
			bulle_ip = packet.readString().decode()

			if self.bulle is not None:
				self.bulle.close()

			self.bulle = Connection('bulle', self, self.loop)
			await self.bulle.connect(bulle_ip, self.main.address[1])
			await self.bulle.send(Packet.new(*CCC).write32(bulle_id))

		elif CCC==(44, 22): # Fingerprint offset changed
			connection.fingerprint = packet.read8()

		elif CCC==(60, 3): # Community platform
			TC = packet.read16()
			self.dispatch('raw_cp', TC, packet.copy(True))
			if TC==3: # Connected to the community platform
				self.dispatch('ready')
			elif TC==65:
				author, message = packet.readUTF(), packet.readString()
				self.dispatch('tribe_message', author, message)
			elif TC==66: # Whisper
				author, commu, receiver, message = packet.readUTF(), packet.read32(), packet.readUTF(), packet.readUTF()
				self.dispatch('whisper', author, commu, receiver, message)
			elif TC==88: # tribe member connected
				self.dispatch('member_connected', packet.readUTF())
			elif TC==90: # tribe member disconnected
				self.dispatch('member_disconnected', packet.readUTF())
			else:
				if self.LOG_UNHANDLED_PACKETS:
					print(CCC, TC, bytes(packet.buffer)[4:])
				return False
		else:
			if self.LOG_UNHANDLED_PACKETS:
				print(CCC, bytes(packet.buffer)[2:])
			return False
		return True

	async def handle_old_packet(self, connection:Connection, oldCCC:tuple, data:list):
		return False

	async def _heartbeat_loop(self):
		"""|coro|
		Send a packet every ten seconds to stay connected to the game.
		"""
		last_heartbeat = 0
		while self.main.open:
			if self.loop.time()-last_heartbeat>=10:
				await self.main.send(Packet.new(26, 26))
				if self.bulle is not None and self.bulle.open:
					await self.bulle.send(Packet.new(26, 26))

				last_heartbeat = self.loop.time()
			await asyncio.sleep(.5)

	def event(self, coro):
		"""A decorator that registers an event.

		More about events [here](Events.md).
		"""
		name = coro.__name__
		if not name.startswith('on_'):
			raise Exception("'{}' isn't a correct event naming.".format(name))
		if not asyncio.iscoroutinefunction(coro):
			raise Exception("Couldn't register a non-coroutine function for the event {}.".format(name))

		setattr(self, name, coro)
		return coro

	def wait_for(self, event, condition=None, timeout=None):
		"""Wait for an event.

		Example: ::
			@client.event
			async def on_room_message(author, message):
				if message=='id':
					await client.sendCommand('profile '+author)
					profile = await client.wait_for('on_profile', lambda p: p.username==author)
					await client.sendRoomMessage('Your id: {}'.format(profile.id))

		:param event: :class:`str` the event name.
		:param condition: Optionnal[:class:`function`] A predicate to check what to wait for. The arguments must meet the parameters of the event being waited for.
		:param timeout: Optionnal[:class:`int`] the number of seconds before raise asyncio.TimeoutError
		:return: :class:`asyncio.Future` a future that you must await.
		"""
		event = event.lower()
		future = self.loop.create_future()

		if condition is None:
			def condition(*a):
				return True

		if event not in self._waiters:
			self._waiters[event] = []

		self._waiters[event].append((condition, future))

		return asyncio.wait_for(future, timeout, loop=self.loop)

	async def _run_event(self, coro, event_name, *args, **kwargs):
		"""|coro|
		Runs an event and handle the error if any.

		:param coro: a coroutine function.
		:param event_name: :class:`str` the event's name.
		:param args: arguments to pass to the coro.
		:param kwargs: keyword arguments to pass to the coro.
		"""
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
		"""Dispatches events

		:param event: :class:`str` event's name. (without 'on_')
		:param args: arguments to pass to the coro.
		:param kwargs: keyword arguments to pass to the coro.
		"""
		method = 'on_' + event

		if method in self._waiters:
			to_remove = []
			waiters = self._waiters[method]
			for i, (cond, fut) in enumerate(waiters):
				if fut.cancelled():
					to_remove.append(i)
					continue

				try:
					result = bool(cond(*args))
				except Exception as e:
					fut.set_exception(e)
				else:
					if result:
						to_remove.append(i)
						fut.set_result(args if len(args) else None)

			if len(to_remove)==len(waiters):
				del self._waiters[method]
			else:
				for i in to_remove[::-1]:
					del waiters[i]

		coro = getattr(self, method, None)
		if coro is not None:
			asyncio.ensure_future(self._run_event(coro, method, *args, **kwargs), loop=self.loop)

	async def start(self, api_tfmid, api_token):
		"""|coro|
		Connects the client to the game.

		:param api_tfmid: :class:`int` or :class:`str` your Transformice id.
		:param api_token: :class:`str` your token to access the API.
		"""
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

	async def login(self, username, password, encrypted=True, room='1'):
		"""|coro|
		Log in the game.

		:param username: :class:`str` the client username.
		:param password: :class:`str` the client password.
		:param encrypted: Optional[:class:`bool`] whether the password is already encrypted or not.
		:param room: Optional[:class:`str`] the room where the client will be logged in.
		"""
		if not encrypted:
			from .utils import shakikoo
			password = shakikoo(password)

		packet = Packet.new(26, 8).writeString(username).writeString(password)
		packet.writeString("app:/TransformiceAIR.swf/[[DYNAMIC]]/2/[[DYNAMIC]]/4")
		packet.writeString(room).write32(self.authkey^self.keys.auth)
		packet.cipher(self.keys.identification).write8(0)

		await self.main.send(packet)

	def run(self, api_tfmid, api_token, username, password, **kwargs):
		"""A blocking call that do the event loop initialization for you.

		Equivalent to ::
			@bot.event
			async def on_login_ready(*a):
				await bot.login(username, password)

			loop = asyncio.get_event_loop()
			loop.create_task(bot.start(api_id, api_token))
			loop.run_forever()
		"""
		asyncio.ensure_future(self.start(api_tfmid, api_token), loop=self.loop)
		self.loop.run_until_complete(self.wait_for('on_login_ready'))
		asyncio.ensure_future(self.login(username, password, **kwargs), loop=self.loop)

		try:
			self.loop.run_forever()
		except Exception as e:
			# add self.close
			# asyncio.ensure_future(self.close())
			raise e

	async def sendCP(self, code, data=b''):
		"""|coro|
		Send a packet to the community platform.

		:param code: :class:`int` the community platform code.
		:param data: :class:`Packet` or :class:`bytes` the data.
		"""
		self.cp_fingerprint = (self.cp_fingerprint + 1) % 0XFFFFFFFF

		packet = Packet.new(60, 3).write16(code)
		packet.write32(self.cp_fingerprint).writeBytes(data)
		await self.main.send(packet, cipher=True)

	async def sendRoomMessage(self, message):
		"""|coro|
		Send a message to the room.

		:param message: :class:`str` the content of the message.
		"""
		packet = Packet.new(6, 6).writeString(message)

		await self.bulle.send(packet, cipher=True)

	async def sendTribeMessage(self, message):
		"""|coro|
		Send a message to the tribe.

		:param message: :class:`str` the content of the message.
		"""
		await self.sendCP(50, Packet().writeString(message))

	async def whisper(self, username, message):
		"""|coro|
		Whisper to a player.

		:param username: :class:`str` the player to whisper.
		:param message: :class:`str` the content of the whisper.
		"""
		await self.sendCP(52, Packet().writeString(username).writeString(message))

	async def getTribe(self, disconnected=True):
		"""|coro|
		Gets the client's :class:`Tribe` and return it

		:param disconnected: :class:`bool` if True retrieves also the disconnected members.
		:return: :class:`Tribe` or ``None``.
		"""
		sid = self.cp_fingerprint + 1
		await self.sendCP(108, Packet().writeBool(disconnected))
		tc, packet = await self.wait_for('on_raw_cp', lambda tc, p: (tc==109 and p.read32()==sid) or tc==130)
		if tc==109:
			result = packet.readByte()
			if result==1:
				tc, packet = await self.wait_for('on_raw_cp', lambda tc, p: tc==130)
			elif result==17:
				return None
			else:
				raise Exception('Internal error: 118-{}'.format(result))
		return Tribe(packet)

	async def sendPrivateMessage(self, username, message):
		"""|coro|
		Deprecated alias for `Client.whisper`.

		:param username: :class:`str` the player to whisper.
		:param message: :class:`str` the content of the whisper.
		"""
		await self.whisper(username, message)

	async def playEmote(self, id, flag='be'):
		"""|coro|
		Play an emote.

		:param id: :class:`int` the emote's id.
		:param flag: Optional[:class:`str`] the flag for the emote id 10. Defaults to 'be'.
		"""
		packet = Packet.new(8, 1).write8(id).write32(0)
		if id==10:
			packet.writeString(flag)

		await self.bulle.send(packet)

	async def sendSmiley(self, id):
		"""|coro|
		Makes the client showing a smiley above it's head.

		:param id: :class:`int` the smiley's id. (from 0 to 10)
		"""
		if 10>id>0:
			raise Exception('Invalid smiley id')

		packet = Packet.new(8, 5).write8(id).write32(0)

		await self.bulle.send(packet)

	async def loadLua(self, lua_code):
		"""|coro|
		Load a lua code in the room.

		:param lua_code: :class:`str` or :class:`bytes` the lua code to send.
		"""
		if isinstance(lua_code, str):
			lua_code = lua_code.encode()

		packet = Packet.new(29, 1).write24(len(lua_code)).writeBytes(lua_code)

		await self.bulle.send(packet)

	async def sendCommand(self, command):
		"""|coro|
		Send a command to the game.

		:param command: :class:`str` the command to send.
		"""
		packet = Packet.new(6, 26).writeString(command)

		await self.main.send(packet, cipher=True)

	async def enterTribe(self):
		"""|coro|
		Enter the tribe house
		"""
		await self.main.send(Packet.new(16, 1))

	async def enterTribeHouse(self):
		"""|coro|
		Alias for :meth:`enterTribe`
		"""
		await self.enterTribe()

	async def joinRoom(self, room_name, community=None, auto=False):
		"""|coro|
		Join a room.
		The event 'on_joined_room' is dispatched when the client has successfully joined the room.

		:param room_name: :class:`str` the room's name.
		:param community: Optional[:class:`int`] the room's community.
		:param auto: Optional[:class:`bool`] joins a random room (I think).
		"""
		packet = Packet.new(5, 38).write8(community or self.community)
		packet.writeString(room_name).writeBool(auto)
		await self.main.send(packet)

	async def enterInvTribeHouse(self, author):
		"""|coro|
		Join the tribe house of another player after receiving an /inv.

		:param author: :class:`str` the author's username who sent the invitation.
		"""
		await self.main.send(Packet.new(16, 2).writeString(author))

	async def recruit(self, player):
		"""|coro|
		Send a recruit request to a player.

		:param player: :class:`str` the player's username you want to recruit.
		"""
		await self.sendCP(78, Packet().writeString(player), cipher=True)
