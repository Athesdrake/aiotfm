import aiohttp

from aiotfm import __version__
from aiotfm.errors import EndpointError, InternalError, MaintenanceError


class Keys:
	"""Represents the keys used by the client to communicate to the server."""
	def __init__(self, **keys):
		self.auth = keys.pop('auth_key', 0)
		self.connection = keys.pop('connection_key', '')
		self.identification = keys.pop('identification_keys', [])
		self.msg = [k & 0xff for k in keys.pop('msg_keys', [])]
		self.packet = keys.pop('packet_keys', [])
		self.version = keys.pop('version', 0)
		self.server_ip = keys.pop('ip', '51.75.130.180')
		self.kwargs = keys


async def get_keys(tfm_id, token):
	"""|coro|
	Fetch the keys required to log into the game.

	:param tfm_id: :class:`int` your Transformice user id.
	:param token: :class:`str` your api token.
	"""
	url = 'https://api.tocuto.tk/get_transformice_keys.php'
	params = {'tfmid': tfm_id, 'token': token}
	headers = {"User-Agent": f"Mozilla/5.0 aiotfm/{__version__}"}

	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params, headers=headers) as resp:
			data = await resp.json()

	success = data.pop('success', False)
	internal_error = data.pop('internal_error', True)
	internal_error_step = data.pop('internal_error_step', 0)
	error = data.pop('error', None)

	if success:
		if not internal_error:
			keys = Keys(**data)
			if len(keys.packet) > 0 and len(keys.identification) > 0 and len(keys.msg) > 0:
				return keys

			raise EndpointError('Something goes wrong: A key is empty ! {}'.format(data))

		if internal_error_step == 2:
			raise MaintenanceError('The game might be in maintenance mode.')

		message = 'An internal error occur: {}'.format(internal_error_step)
		raise InternalError(message)

	raise EndpointError("Can't get the keys. Error info: {}".format(error))
