import aiotfm
import asyncio
import os
import pytest

from aiotfm import Client
from aiotfm.inventory import InventoryItem
from aiotfm.shop import Shop


class Bot(Client):
	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)
		self.is_ready = False

	async def on_login_result(self, *args): # pragma: no cover
		pass # disable the default handler

	async def on_ready(self):
		self.is_ready = True


@pytest.fixture(scope='module')
def event_loop():
	loop = asyncio.get_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='module')
def bot():
	return Bot()


pytestmark = pytest.mark.asyncio


def abort_on_failure(func):
	async def wrapper(bot: Client): # pragma: no cover
		try:
			await func(bot)
		except Exception:
			pytest.exit('Cannot setup the client instance. Aborting the tests...')

	return wrapper


@abort_on_failure
async def test_get_keys(bot: Client):
	api_id, api_token = os.environ.get('AIOTFM_API_KEYS', ':').split(':')
	assert api_id != ''
	assert api_token != ''

	bot.keys = await aiotfm.utils.get_keys(api_id, api_token)


@abort_on_failure
async def test_connect(bot: Client):
	await bot.connect()


@abort_on_failure
async def test_handshake(bot: Client):
	fut: asyncio.Future = bot.wait_for('on_login_ready', timeout=3)
	await bot.sendHandshake()

	print('on_login_ready', await fut)


async def test_login(bot: Client):
	username, password = os.environ.get('AIOTFM_TEST_CLIENT', ':').split(':')
	assert username != ''
	assert password != ''

	fut: asyncio.Future = bot.wait_for('on_login_result', timeout=3)
	await bot.login(username, password, encrypted=True, room='*aiotfm')

	with pytest.raises(asyncio.TimeoutError):
		code, *_ = await fut


async def test_join_room(bot: Client):
	fut: asyncio.Future = bot.wait_for('on_joined_room', timeout=3)
	await bot.joinRoom('*aiotfmtest')

	room = await fut
	assert room.name == '*aiotfmtest'


async def test_room_message(bot: Client):
	def condition(msg):
		return msg.author == bot.username

	fut: asyncio.Future = bot.wait_for('on_room_message', condition, timeout=3)
	await bot.sendRoomMessage('[[aiotfm test]]')

	msg: aiotfm.message.Message = await fut
	assert msg.content == '[[aiotfm test]]'
	assert '[[aiotfm test]]' in str(msg)


async def test_profile(bot: Client):
	fut: asyncio.Future = bot.wait_for('on_profile', timeout=3)
	await bot.sendCommand(f'profile {bot.username}')

	profile: aiotfm.Profile = await fut
	assert profile.username == bot.username
	assert aiotfm.Player(bot.username, uid=profile.id) == aiotfm.Player(bot.username, uid=profile.id)
	assert not aiotfm.Player(bot.username).isGuest
	assert aiotfm.Player("*Souris").isGuest


async def test_shop(bot: Client):
	fut: asyncio.Future = bot.wait_for('on_shop', timeout=3)
	await bot.requestShopList()
	shop: Shop = await fut

	d = shop.to_dict()
	assert shop.cheese == d['cheese']
	assert shop.fraise == d['fraise']
	assert shop.look == d['look']


async def test_room_list(bot: Client):
	roomlist = await bot.getRoomList()
	assert roomlist is not None

	await asyncio.sleep(3)
	roomlist = await bot.getRoomList(aiotfm.enums.GameMode.MODULES)
	assert roomlist is not None
	assert len(roomlist.pinned_rooms) > 0
	assert isinstance(roomlist.pinned_rooms[0], aiotfm.room.DropdownRoomEntry)


async def test_inventory(bot: Client):
	if bot.inventory is None: # pragma: no cover
		fut: asyncio.Future = bot.wait_for('on_inventory_update', timeout=3)
		await bot.requestInventory()
		await fut

	with pytest.raises(TypeError):
		bot.inventory['crash']

	with pytest.raises(KeyError):
		bot.inventory[999999]

	with pytest.raises(TypeError):
		bot.inventory['crash'] = 123

	# should throw an error:
	# bot.inventory[999999] = 132

	item = bot.inventory.get(800)

	assert item.is_currency
	assert item.image_url == 'https://www.transformice.com/images/x_transformice/x_inventaire/800.jpg'
	assert item.can_use == (item.quantity > 0)
	assert item == InventoryItem(800)
	assert all(i.is_equipped for i in bot.inventory.getEquipped())

	with pytest.raises(TypeError):
		await bot.inventory.get(0).use()

	assert len(bot.inventory.sort()) == len(bot.inventory.items)


async def test_channel(bot: Client):
	if not bot.is_ready: # pragma: no cover
		await bot.wait_for('on_ready', timeout=5)

	def condition(msg):
		return msg.author == bot.username

	fut: asyncio.Future = bot.wait_for('on_channel_joined', timeout=3)
	await bot.joinChannel('aiotfmtest', permanent=False)

	channel: aiotfm.message.Channel = await fut
	assert channel.name == 'aiotfmtest'
	assert bot.username in await channel.who()

	fut: asyncio.Future = bot.wait_for('on_channel_message', condition, timeout=3)
	await channel.send('[[aiotfm test]]')

	msg: aiotfm.message.ChannelMessage = await fut
	assert msg.content == '[[aiotfm test]]'
	assert msg.channel == channel
	assert '[[aiotfm test]]' in str(msg)

	await msg.reply('Working!')

	fut: asyncio.Future = bot.wait_for('on_channel_left_result', timeout=3)
	await channel.leave()

	sequenceId, result = await fut
	assert result == 1


async def test_whisper(bot: Client):
	for i in range(5):
		fut: asyncio.Future = bot.wait_for('on_whisper', timeout=3)
		await bot.whisper(bot.username, '[[aiotfm test]]')
		msg: aiotfm.message.Whisper = await fut

		assert msg.author == bot.username
		assert msg.receiver == bot.username
		assert msg.content == '[[aiotfm test]]'
		assert msg.sent
		assert '[[aiotfm test]]' in str(msg)

		await asyncio.sleep(1.5)
		await msg.reply('Working!')
		await asyncio.sleep(1.5)


async def test_tribe_message(bot: Client):
	def condition(author, message):
		return author.lower() == bot.username.lower()

	fut: asyncio.Future = bot.wait_for('on_tribe_message', condition, timeout=3)
	await bot.sendTribeMessage('[[aiotfm test]]')
	_, message = await fut

	assert message == '[[aiotfm test]]'


async def test_friend_list(bot: Client):
	if bot.friends is None:
		bot.wait_for('on_friends_loaded', timeout=3)

	friends = [f.name.lower() for f in bot.friends]
	print(friends)

	assert 'athesdrake#0000' in friends


async def test_tribe(bot: Client):
	tribe = await asyncio.sleep(3)
	tribe = await bot.getTribe()

	if tribe is not None:
		assert len(tribe.members) > 0
		tribe = await bot.getTribe(True)
		assert len(tribe.members) > 0


async def test_emote(bot: Client):
	await bot.playEmote(10)


async def test_smiley(bot: Client):
	await bot.sendSmiley(5)


async def test_tribe_house(bot: Client):
	fut: asyncio.Future = bot.wait_for('on_joined_room', timeout=3)
	await bot.enterTribe()
	room: aiotfm.room.Room = await fut

	assert room.is_tribe


async def test_lua(bot: Client):
	fut: asyncio.Future = bot.wait_for('on_lua_log', timeout=3)
	await bot.loadLua("print('[[aiotfm test]]')")
	log = await fut
	assert '[[aiotfm test]]' in log


async def test_command(bot: Client):
	pytest.skip()
	fut: asyncio.Future = bot.wait_for('on_server_message', timeout=3)
	await bot.sendCommand('ping')
	message = await fut
	assert 'ms' in message


async def test_abort(bot: Client):
	bot.bulle.abort()


async def test_close(bot: Client):
	bot.close()
	await bot.main.send(b'')
	while not bot._hb_task.done():
		await asyncio.sleep(.1)
