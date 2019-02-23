import asyncio
import json

from aiotfm.client import Client

with open('bot.config') as f:
	config = json.load(f)

bot = Client()

boot_time = bot.loop.time()

@bot.event
async def on_login_ready(*a):
	print('Logging in ...')
	await bot.login(**config)

@bot.event
async def on_ready():
	print('Connected to the community platform in {:.2f} seconds'.format(bot.loop.time()-boot_time))
	await bot.enterTribe()

@bot.event
async def on_tribe_inv(author, tribe):
	print('tribe invitation received')
	await bot.enterInvTribeHouse(author)

@bot.event
async def on_whisper(author, commu, receiver, message):
	if message=='tribe':
		await bot.enterTribeHouse()
	await bot.whisper(author, message) # echo

@bot.event
async def on_room_message(author, message):
	print('[{}] {}'.format(author.decode(), message.decode()))
	if message=='tribe':
		await bot.enterTribeHouse()

@bot.event
async def on_joined_room(room_name, is_private):
	print('Joined room:', room_name.decode(), is_private)

loop = asyncio.get_event_loop()
loop.create_task(bot.start(config.pop('api_id'), config.pop('api_token')))

loop.run_forever()