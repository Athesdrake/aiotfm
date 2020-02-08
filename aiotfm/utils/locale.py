import re
import zlib
import aiohttp

from aiotfm.errors import InvalidLocale


class Translation:
	"""Represents a translation item of the game.

	Parameters
	----------
	key: :class:`str`
		The translation's key.
	value: :class:`str`
		The translated text.

	Attributes
	----------
	key: :class:`str`
		The translation's key.
	value: :class:`str`
		The translated text.
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __str__(self):
		return self.value

	def __repr__(self):
		return f'{self.key}={self.value}'

	def format(self, *args):
		"""Format the translation value, replacing %N place holders by arguments.

		:params: the values to inject.
		:return: :class:`str` the formatted output."""
		def repl(match):
			index = int(match.group(1))
			if index > len(args) or index == 0:
				return match.group(0)
			return str(args[index - 1])

		return re.sub(r'%(\d+)', repl, self.value)


class Locale:
	"""Represents the locale file of the game.

	Parameters
	----------
	locale: :class:`str`
		The locale name.

	Attributes
	----------
	locales: :class:`dict`[:class:`aiotfm.locale.Locale`]
		Cached locales.
	locale: :class:`str`
		The locale name.
	"""
	BASE_URL = 'http://transformice.com/langues/tfz_{}'

	def __init__(self, locale='en'):
		self._locale = locale
		self.locales = {}

	def __getitem__(self, key):
		"""Return the translation of a key.

		:param key: :class:`str` the translation's key
		:return: :class:`aiotfm.locale.Translation`
		"""
		table = self.locales.get(self.locale, {})
		value = table.get(key[1:] if key[0] == '$' else key, None)

		if value is None:
			return Translation(key, key)

		return Translation(key, value)

	@property
	def locale(self):
		"""The active locale."""
		return self._locale

	async def reload(self, locale=None):
		"""|coro|
		Reload a locale and set it as active.

		:param locale: Optional[:class:`str`] The locale name you want to reload.
			If it's None, the active locale is used instead.
		"""
		if locale is None:
			locale = self._locale

		# Deletes the locale then load it
		del self.locales[locale]
		await self.load(locale)

	async def load(self, locale=None):
		"""|coro|
		Load a locale and set it as active.

		:param locale: Optional[:class:`str`] The locale name you want to load.
			If it's None, the active locale is used instead.
		"""
		if locale is not None:
			self._locale = locale

		# Check if the locale is cached
		if self._locale in self.locales:
			return

		# Download the locale
		async with aiohttp.ClientSession() as session:
			async with session.get(self.BASE_URL.format(self._locale)) as r:
				if r.status == 404:
					raise InvalidLocale()

				# Decompress the file and parse it
				content = zlib.decompress(await r.read()).decode('utf-8')
				table = {k: v for k, v in (t.split('=', 1) for t in content.split('¤') if t)}
				# Add the translation table
				self.locales[self._locale] = table