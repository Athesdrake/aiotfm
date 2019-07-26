import aiotfm
import asyncio
import json


class Bot(aiotfm.Client):
	def __init__(self, community=0):
		super().__init__(community)

		self.room = None
		self.username = None
		self.pid = 0

	async def handle_packet(self, conn, packet):
		handled = await super().handle_packet(conn, packet.copy())

		if not handled: # Add compatibility to more packets
			CCC = packet.readCode()

			if CCC==(60, 4): # Tribulle V2 enabled
				print(f'Tribulle 2 : {packet.readBool()}')

	async def getProfile(self, username, timeout=3):
		username = username.lower()
		try:
			await self.sendCommand('profile {}'.format(username))
			return await self.wait_for('on_profile', lambda p: p.username.lower()==username, timeout=timeout)
		except asyncio.TimeoutError:
			return None # The player does not exists or is not connected.

	async def on_login_ready(self, online_players, community, country):
		print('Connected to Transformice.')
		print(f'There are {online_players} online players.')
		print(f'Received {community}-{country} as community.')

		with open('bot.config') as f:
			config = json.load(f)
			kwargs = {p:config.get(p) for p in ['password', 'encrypted', 'room'] if config.get(p, None) is not None}
			self.username = config.get('username')

			await self.login(self.username, **kwargs)

	async def on_logged(self, player_id, username, played_time, community, pid):
		self.username = username
		self.pid = pid

	async def on_ready(self):
		print('Connected to the community platform.')
		while self.room is None or '\x03' not in self.room:
			await self.enterTribeHouse()
			try:
				await self.wait_for('on_joined_room', timeout=3)
			except:
				pass

	async def on_joined_room(self, room, private):
		self.room = room.decode() if isinstance(room, bytes) else room
		print(f'Joined room [{self.room}]')

	async def on_whisper(self, message):
		print(message)
		if message.author!=self.username and message.content.startswith('!'):
			await self.execute(message, *message.content[1:].split(' '))

	async def execute(self, msg, cmd, *args):
		if cmd=='hi':
			await msg.reply("Hoi!")
		elif cmd=='firsts':
			name = msg.author if len(args)<1 else args[0]
			profile = await self.getProfile(name)
			if profile is None:
				await self.reply("The player doesn't exists or is'nt connected.")
			else:
				await self.reply(f"{profile.username} has {profile.stats.firsts} firsts.")


if __name__ == '__main__':
	bot = Bot()
	bot.run()