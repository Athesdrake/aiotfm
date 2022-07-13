import aiohttp

from aiotfm import __version__
from aiotfm.errors import EndpointError, InternalError, MaintenanceError


class Keys:
	"""Represents the keys used by the client to communicate to the server."""
	def __init__(self, **keys):
		self.auth = keys.pop('auth', 0)
		self.connection = keys.pop('connection', '')
		self.identification = keys.pop('identification', [])
		self.msg = [k & 0xff for k in keys.pop('msg', [])]
		self.packet = keys.pop('packet', [])
		self.version = keys.pop('version', 0)
		self.server_ip = keys.pop('ip', '193.70.81.30')
		self.server_ports = keys.pop('ports', [11801, 12801, 13801, 14801])
		self.kwargs = keys


async def request_api(url):
	"""|coro|
	Sends a GET request to the specified URL, expecting a JSON response.
	If the client is unable to receive a proper JSON response,
	an empty dictionary is returned.

	:param url: :class:`str` The URL to send the request to.
	"""
	headers = {"User-Agent": f"Mozilla/5.0 aiotfm/{__version__}"}

	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=headers) as resp:
				return await resp.json()
	except aiohttp.ClientError:
		return {}


async def get_ip():
	"""|coro|
	Fetch the game IP and ports, useful for bots with the official role.
	"""
	url = 'https://cheese.formice.com/api/tfm/ip'
	data = await request_api(url)

	if not len(data):
		# Empty dictionary, request failed, let's use default server IP
		success = True
	else:
		success = data.pop('success', False)
		error = data.pop('error', '').capitalize()
		description = data.pop('description', 'No description was provided.')

	if not success:
		if error == 'Maintenance':
			raise MaintenanceError('The game is under maintenance.')

		if error == 'Internal':
			raise InternalError(description)

		raise EndpointError(f'{error}: {description}')

	return Keys(version=666, **data.get('server', {}))


async def get_keys(tfm_id, token):
	"""|coro|
	Fetch the keys required to log into the game.

	:param tfm_id: :class:`int` your Transformice user id.
	:param token: :class:`str` your api token.
	"""
	url = f'https://api.tocuto.tk/tfm/get/keys/{tfm_id}/{token}'
	data = await request_api(url)

	success = data.pop('success', False)
	error = data.pop('error', '').capitalize()
	description = data.pop('description', 'No description was provided.')

	if not success:
		if error == 'Maintenance':
			raise MaintenanceError('The game is under maintenance.')

		if error == 'Internal':
			raise InternalError(description)

		raise EndpointError(f'{error}: {description}')

	keys = Keys(**data.get('server', {}), **data.get('keys', {}))
	if len(keys.packet) > 0 and len(keys.identification) > 0 and len(keys.msg) > 0 and keys.version != 0:
		return keys

	raise EndpointError('Something went wrong: A key is empty ! {}'.format(data))
