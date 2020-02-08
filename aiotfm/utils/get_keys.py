import aiohttp

from aiotfm import __version__
from aiotfm.errors import EndpointError, InternalError, MaintenanceError


class Keys:
	"""Represents the keys used byt the client to communicate to the server."""
	def __init__(self, version, connection_key, auth_key, packet_keys, identification_keys, msg_keys):
		self.version = version
		self.connection = connection_key
		self.auth = auth_key
		self.packet = packet_keys
		self.identification = identification_keys
		self.msg = msg_keys


async def get_keys(tfm_id, token):
	"""|coro|
	Fetch the keys required to log into the game.

	:param tfm_id: :class:`int` your Transformice user id.
	:param token: :class:`str` your api token.
	"""
	url = 'https://api.tocu.tk/get_transformice_keys.php'
	params = {'tfmid': tfm_id, 'token': token}
	headers = {"User-Agent": f"Mozilla/5.0 aiotfm/{__version__}"}

	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params, headers=headers) as resp:
			data = await resp.json()

	if data.get('success', False):
		if not data.get('internal_error', True):
			keys = Keys(**data)
			if len(keys.packet) > 0 and len(keys.identification) > 0 and len(keys.msg) > 0:
				return keys

			raise EndpointError('Something goes wrong: A key is empty ! {}'.format(data))

		if data.get('internal_error_step') == 2:
			raise MaintenanceError('The game might be in maintenance mode.')

		message = 'An internal error occur: {}'.format(data.get('internal_error_step'))
		raise InternalError(message)

	raise EndpointError("Can't get the keys. Error info: {}".format(data.get('error')))