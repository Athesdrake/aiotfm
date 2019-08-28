from aiotfm import __version__
from aiotfm.errors import EndpointError, InternalError, MaintenanceError

try:
	import aiohttp
except ImportError:
	import json
	from urllib import request

	_AIOHTTP = False
else:
	_AIOHTTP = True


async def get_keys(tfm_id, api_token):
	url = 'https://api.tocu.tk/get_transformice_keys.php?tfmid={}&token={}'.format(tfm_id, api_token)
	headers = {"User-Agent": f"Mozilla/5.0 aiotfm/{__version__}"}

	if _AIOHTTP:
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=headers) as resp:
				data = await resp.json()
	else:
		print('WARNING: aiohttp is unavailable urllib is used instead. use of aiohttp is highly recommended.The')
		result = request.urlopen(request.Request(url, headers=headers)).read()
		data = json.loads(result)

	if data.get('success', False):
		if not data.get('internal_error', True):
			class keys:
				version = data.get('version')
				connection = data.get('connection_key')
				auth = data.get('auth_key')
				packet = data.get('packet_keys')
				identification = data.get('identification_keys')
				msg = data.get('msg_keys')

			if len(keys.packet) and len(keys.identification) and len(keys.msg):
				return keys

			raise EndpointError('Something goes wrong: A key is empty ! {}'.format(data))
		else:
			if data.get('internal_error_step')==2:
				raise MaintenanceError('The game might be in maintenance mode.')
			else:
				raise InternalError('An internal error occur: {}'.format(data.get('internal_error_step')))
	else:
		raise EndpointError("Can't get the keys. Error info: {}".format(data.get('error')))