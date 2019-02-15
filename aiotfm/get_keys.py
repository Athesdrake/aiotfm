import aiohttp

async def get_keys(tfm_id, api_token):
	url = 'https://api.tocu.tk/get_transformice_keys.php?tfmid={}&token={}'.format(tfm_id, api_token)
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			data = await resp.json()
	# result = request.urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"})).read()
	# data = json.loads(result)

	if data['success']:
		if not data['internal_error']:
			class keys:
				version = data['version']
				connection = data['connection_key']
				auth = data['auth_key']
				packet = data['packet_keys']
				identification = data['identification_keys']
				msg = data['msg_keys']
			return keys
		else:
			if data['internal_error_step']==2:
				raise Exception('The game might be in maintenance mode.')
			else:
				raise Exception('An internal error occur: {}'.format(data['internal_error_step']))
	else:
		raise Exception("Can't get the keys. Error info: {}".format(data['error']))