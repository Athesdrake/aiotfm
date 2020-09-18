import aiotfm
import asyncio
import json
import os
import re
from Notifier import Notifier
from aiotfm.client import Client

from dotenv import load_dotenv
load_dotenv()

config = {
	'username': 'Nofeet#9658',
	'password': os.environ['password'],
	'encrypted': False,
	'room': '*#Yionutz',
	'api_id': 10187511,
	'api_token': os.environ['api_token']
}

bot = Client()

boot_time = bot.loop.time()


@bot.event
async def on_login_ready(*a):
	print('Logging in ...')
	await bot.login(**config)


@bot.event
async def on_ready():
	print(f'Connected to the community platform in {bot.loop.time() - boot_time:.2f} seconds')
	await bot.enterTribe()
	# while not bot.room.is_tribe:
	# 	await bot.enterTribeHouse()
	# 	try:
	# 		await 		bot.wait_for('on_joined_room', timeout=3)
	# 	except asyncio.TimeoutError:
	# 		pass


@bot.event
async def on_tribe_inv(author, tribe):
	print('tribe invitation received')
	await bot.enterInvTribeHouse(author)


@bot.event
async def on_whisper(message):
	print(message)
	# if message.content == 'tribe':
	# 	await bot.enterTribeHouse()
	# await message.reply(message.content) # echo

	if message.author != bot.username and message.content.startswith('!'):
		await execute(message, *message.content[1:].split(' '))


@bot.event
async def on_room_message(message):
	print(message)
	if message.content == 'tribe':
		await bot.enterTribeHouse()


@bot.event
async def on_joined_room(room):
	print('Joined room:', room)

	if room.name == "*Ancienius":
		await bot.sendCommand("module deathmatch")
		print('done')
	else:
		while not room.is_tribe:
			await bot.enterTribeHouse()
			try:
				await bot.wait_for('on_joined_room', timeout=3)
			except asyncio.TimeoutError:
				pass


async def processRestarting():
	while True:
		await asyncio.sleep(3600.0)
		print("Restarting transformice bot", flush=True)


@bot.event
async def on_eventNewGame(npCode):
	if npCode == 6627689:
		await bot.sendCommand("module deathmatch")

async def on_server_restart(restartIn):
	print(f"[Server] restart in {restartIn}")


@bot.event
async def on_channel_message(message):
	if message.channel.name == 'dmStaff-GqAeYoZ' and bot.room.name == "*Ancienius":
		if message.author != bot.username and message.content.startswith('!'):
			await execute(message, *message.content[1:].split(' '))

async def execute(msg, cmd, *args):
	if cmd == 'find' and len(args)>0:
		name = args[0]
		await bot.sendRoomMessage(f"!find {name}")


@bot.event
async def on_receive_textArea(id, content):
	if id == 1497:
		if content.startswith('x1Tz0@'):
			notifier = Notifier(content)


@bot.event
async def on_lua_chat_message(message):
	print(message.content)
	if bool(re.compile(".*</G><font color='#ff9478'>.*? farmer</font>").match(message.content)):
		r = re.findall("<font *.*?>(.*?)</font>", message.content)
		await bot.sendChannelMessage('dmStaff-GqAeYoZ', f"[{r[0][:-1]}] -> {r[1]}")

# @bot.event
# async def on_raw_socket(connection, packet):
# 	print(packet)
# 	print(packet.readCode())
# 	print('end')


loop = asyncio.get_event_loop()
loop.create_task(bot.start(config.pop('api_id'), config.pop('api_token')))

loop.run_forever()