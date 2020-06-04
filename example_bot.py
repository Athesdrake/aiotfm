import asyncio
import json
from time import sleep
import os

from aiotfm.client import Client
from aiotfm.message import Channel


from Notifier import Notifier

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
	print(
			f'Connected to the community platform in {bot.loop.time() - boot_time:.2f} seconds')
	# await bot.sendChannelMessage("dmStaff-GqAeYoZ", "hi :D")
	sleep(6)
	await bot.enterTribe()
	#await bot.joinRoom("#Yionutz","tdl")

@bot.event
async def on_restart():
	print("restarting the bot...")


@bot.event
async def on_tribe_inv(author, tribe):
	print('tribe invitation received')
	# await bot.enterInvTribeHouse(author)


@bot.event
async def on_whisper(message):
	if message.author=="Yionutz#00000" and message.content == 'moduledm':
		await bot.sendCommand("module deathmatch")
		await message.reply("done")
	if message.author=="Yionutz#00000" and message.content == 'tribe':
		await bot.enterTribeHouse()
		await message.reply("done")


@bot.event
async def on_room_message(message):
	print(message)
	# if message.content == 'tribe':
	# await bot.sendCommand("module deathmatch")


@bot.event
async def on_channel_message(message):
	if message.channel.name == 'dmStaff-GqAeYoZ':
		print(message)


@bot.event
async def on_joined_room(room):
	if room.name == "*Ancienius":
		await bot.sendCommand("module deathmatch")

@bot.event
async def on_lua_chat_message(message):
	#print(message)
	if message.content.startswith('x1Tz0@'):
		print("test")

@bot.event
async def on_receive_textArea(id, content):
	if id == 1497:
		if content.startswith('x1Tz0@'):
			notifier = Notifier(content)

# @bot.event
# async def on_raw_socket(connection, packet):
#     print(packet)
#     print(packet.readCode())
#     print('end')


loop = asyncio.get_event_loop()
loop.create_task(bot.start(config.pop('api_id'), config.pop('api_token')))

loop.run_forever()