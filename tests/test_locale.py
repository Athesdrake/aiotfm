import pytest

from aiotfm.utils import Locale


_locale = None


@pytest.fixture
def locale():
	global _locale
	if _locale is None:
		_locale = Locale()

	return _locale


pytestmark = pytest.mark.asyncio


async def test_load(locale: Locale):
	await locale.load()


async def test_reload(locale: Locale):
	await locale.reload()
	await locale.reload('en')


async def test_load_another(locale: Locale):
	await locale.load('fr')


async def test_load_cache(locale: Locale):
	await locale.load('en')
