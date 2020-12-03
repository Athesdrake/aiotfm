import aiotfm
import pytest

from aiotfm.utils import Date, get_keys, shakikoo
from aiotfm.utils import Locale


def test_date():
	date = Date(2020, 6, 25)
	assert date == Date.fromtimestamp(date.timestamp())


async def test_keys():
	with pytest.raises(aiotfm.errors.EndpointError):
		await get_keys('', '')


def test_shakikoo():
	shakikoo('password123') == b'VWVXKV+t6UtkQta9b5b4C8ZY26cAC2tEV6IKct+noTg='


async def test_locale():
	locale = Locale()

	await locale.load()

	assert locale.locale == 'en'
	assert str(locale['T_0']) == str(locale['$T_0']) == 'Little Mouse'
	assert str(locale['shouldnotexists']) == 'shouldnotexists'
	assert repr(locale['shouldnotexists']) == 'shouldnotexists=shouldnotexists'
	assert locale['texte.version.valeur'].format() == 'Version %1'
	assert locale['texte.version.valeur'].format(125) == 'Version 125'

	with pytest.raises(aiotfm.errors.InvalidLocale):
		await locale.load('something invalid')
