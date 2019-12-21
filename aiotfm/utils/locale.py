import aiohttp
import re
import zlib

from aiotfm.errors import InvalidLocale

class Translation:
	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __str__(self):
		return self.value

	def __repr__(self):
		return f'{self.key}={self.value}'

	def format(self, *args):
		def repl(match):
			index = int(match.group(1))
			if index>len(args) or index==0:
				return match.group(0)
			return str(args[index-1])

		return re.sub(r'%(\d+)', repl, self.value)

class Locale:
	BASE_URL = 'http://transformice.com/langues/tfz_{.locale}'

	def __init__(self, locale='en'):
		self._locale = locale
		self.locales = {}

	def __getitem__(self, key):
		table = self.locales.get(self.locale, {})
		value = table.get(key[1:] if key[0]=='$' else key, None)

		if value is None:
			return Translation(key, key)

		return Translation(key, value)

	@property
	def locale(self):
		return self._locale

	async def reload(self, locale=None):
		if locale is None:
			locale = self.locale

		# Deletes the locale then load it
		del self.locales[locale]
		await self.load(locale)

	async def load(self, locale=None):
		if locale is not None:
			self._locale = locale

		# Check if the locale is cached
		if locale in self.locales:
			return

		# Download the locale
		async with aiohttp.ClientSession() as session:
			async with session.get(self.BASE_URL.format(self)) as r:
				if r.status==404:
					raise InvalidLocale()

				# Decompress the file and parse it
				content = zlib.decompress(await r.read()).decode('utf-8')
				table = {k:v for k,v in [t.split('=', 1) for t in content.split('¤') if t]}
				# Add the translation table
				self.locales[locale] = table