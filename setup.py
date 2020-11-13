import re
import setuptools

with open('aiotfm/__version__.py') as f:
	match = re.search(r'__version__ = (["\'])([^"\']+)\1', f.read())
	version = match.group(2)

with open('requirements.txt') as f:
	requirements = f.readlines()
with open('README.md') as f:
	README = f.read()

setuptools.setup(
	name='aiotfm',
	version=version,
	packages=['aiotfm', 'aiotfm.utils'],
	author='Athesdrake',
	description="An asynchronous event based client for Transformice.",
	long_description=README,
	long_description_content_type='text/markdown',
	url='https://github.com/Athesdrake/aiotfm',
	install_requires=requirements,
	python_requires='>=3.6',
	keywords=['TRANFORMICE', 'CLIENT', 'ASYNC', 'ATELIER801', 'EVENT'],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Framework :: AsyncIO",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Topic :: Software Development :: Libraries",
	]
)
