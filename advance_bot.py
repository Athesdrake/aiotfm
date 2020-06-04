import aiotfm
import asyncio
import json
import os

from Notifier import Notifier

#from dotenv import load_dotenv
#load_dotenv()

config = {
	'username': 'Nofeet#9658',
	'password': os.environ['password'],
	'encrypted': False,
	'room': '*#Yionutz',
	'api_id': 10187511,
	'api_token': os.environ['api_token']
}

class Bot(aiotfm.Client):
	def __init__(self, community=0):
		super().__init__(community)
		self.pid = 0

	async def handle_packet(self, conn, packet):
		handled = await super().handle_packet(conn, packet.copy())

		if not handled: # Add compatibility to more packets
			CCC = packet.readCode()

			if CCC == (60, 4): # Tribulle V2 enabled
				print(f'Tribulle 2 : {packet.readBool()}')

	async def getProfile(self, username, timeout=3):
		username = username.lower()

		def check(p):
			if '#' not in username:
				return p.username.split('#')[0].lower() == username
			return p.username.lower() == username

		try:
			await self.sendCommand('profile {}'.format(username))
			return await self.wait_for('on_profile', check, timeout=timeout)
		except asyncio.TimeoutError:
			return None

	def run(self, block=True):
		api_id, api_token = config.pop('api_id'), config.get('api_token')

		self.loop.run_until_complete(self.start(api_id, api_token))
		if block:
			self.loop.run_forever()

	async def on_login_ready(self, online_players, community, country):
		print('Connected to Transformice.')
		print(f'There are {online_players} online players.')
		print(f'Received {community}-{country} as community.')
		username = config.get('username')
		password = config.get('password')
		kwargs = {k: config.get(k) for k in ('encrypted', 'room') if config.get(k) is not None}

		await self.login(username, password, **kwargs)

	async def on_logged(self, player_id, username, played_time, community, pid):
		self.pid = pid

	async def on_ready(self):
		print('Connected to the community platform.')
		while not self.room.is_tribe:
			await self.enterTribeHouse()
			try:
				await self.wait_for('on_joined_room', timeout=3)
			except asyncio.TimeoutError:
				pass

	async def on_joined_room(self, room):
		self.room = room.decode() if isinstance(room, bytes) else room
		print(f'Joined room [{self.room}]')
		if self.room.name == "*Ancienius":
			await self.sendCommand("module deathmatch")
			print('done')

	async def on_whisper(self, message):
		print(message)
		if message.author != self.username and message.content.startswith('!'):
			await self.execute(message, *message.content[1:].split(' '))

	async def execute(self, msg, cmd, *args):
		if cmd == 'hi':
			await msg.reply("Hoi!")
		elif cmd == 'firsts':
			name = str(msg.author) if len(args) < 1 else args[0]
			profile = await self.getProfile(name)
			if profile is None:
				await msg.reply("The player doesn't exists or isn't connected.")
			else:
				await msg.reply(f"{profile.username} has {profile.stats.firsts} firsts.")

	async def on_receive_textArea(self, id, content):
		if id == 1497:
			if content.startswith('x1Tz0@'):
				notifier = Notifier(content)

if __name__ == '__main__':
	bot = Bot()
	bot.run()