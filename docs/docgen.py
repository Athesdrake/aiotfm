import ast
import re
import weakref

from ast import ClassDef, FunctionDef, AsyncFunctionDef


link_regex = re.compile(r'^\.{2}\s*_([^:]+):\s*(https?://(?:\w+\.)+\w+(?:/[.\w-]*)*)')
link_ref_regex = re.compile(r'`([^`]+)`_')
params_regex = re.compile(r'\n([^:\n]+):\s*([^\n]+)((?:\n\s+(?:[^\n]+))+)')
params_doc_regex = re.compile(r':param (\w+): (.+)')
type_regex_op = re.compile(r'(?:(Optional)\[)?(?::(class|meth):`)?([^`]+)(?(2)`)(?(1)\])')
type_regex = re.compile(r':(class|meth):`([^`]+)`')
codeblock_regex = re.compile(r'\n(\w+): ::((?:\n+\t[^\n]+)+)')

class Type:
	def __init__(self, name, type_, optional=False):
		self.name = name
		self.type = type_
		self.isOptional = optional

	def __str__(self):
		name = self.name.split('.')[-1]
		if self.name in dir(__builtins__) or self.type is None:
			return f'`{name}`'

		link = self.name.replace(' ', '-')
		parts = link.split('.')
		if len(parts) > 1 and parts[0] == 'aiotfm':
			parts[1] = parts[1].title()
			link = f'{parts[1]}.md'
			anchor = ".".join(parts[2:])
			if len(anchor) > 0:
				anchor = '#' + anchor

			return f'[`{name}`]({link})'

		link = link.lower().replace('.', '')
		return f'[`{name}`](#{link})'

	def __repr__(self):
		name = self.name
		if self.type is not None:
			name = f':{self.type}:`{name}`'

		if self.isOptional:
			return f'Optional[{name}]'

		return name

	@classmethod
	def parse(cls, string):
		optional, type_, name = type_regex_op.search(string).groups()
		return cls(name, type_, optional is not None)


def parse_params(doc):
	params = list(map(list, params_regex.findall(doc)))
	for param in params:
		param[1] = Type.parse(param[1])
		param[2] = re.sub(r'\s+', ' ', param[2])

	return params


def parse_fdoc(doc):
	params = list(map(list, params_doc_regex.findall(doc)))
	for param in params:
		param[1] = format(re.sub(r'\s+', ' ', param[1].strip('\n')), {})

	return params


def format(string, links):
	def repl_types(m):
		type_, name = m.groups()
		if name in dir(__builtins__):
			return f'`{name}`'

		link = name.replace(' ', '-')
		name = name.split('.')[-1]
		parts = link.split('.')

		if len(parts) > 1 and parts[0] == 'aiotfm':
			parts[1] = parts[1].title()
			link = f'{parts[1]}.md'
			anchor = ".".join(parts[2:])
			if len(anchor) > 0:
				anchor = '#' + anchor

			return f'[`{name}`]({link})'

		link = link.lower().replace('.', '')
		return f'[`{name}`](#{link})'

	def repl_links(m):
		name = m.group(1)
		if name in links:
			return f'[`{name}`]({links[name]})'
		return m.group(0)[:-1]

	return link_ref_regex.sub(repl_links, type_regex.sub(repl_types, string))


def deploy_codeblock(string):
	def repl(match):
		name, code = match.groups()
		code = code.replace('\n\t', '\n').strip('\n')
		return f'\n__{name}__:\n```Python\n{code}\n```'

	return codeblock_regex.sub(repl, string)


def signature(func):
	args = []
	args.extend(a.arg for a in func.args.args)
	# print(func.args._fields)

	if func.args.vararg is not None:
		args.append('*args')

	defaults = func.args.kw_defaults
	args.extend(f'{a.arg}={defaults[i].value}' for i, a in enumerate(func.args.kwonlyargs))

	if func.args.kwarg is not None:
		args.append('**kwargs')

	return ', '.join(args)


def generate(filename, name):
	with open(filename, 'r', encoding='utf-8') as f:
		code: ast.Module = ast.parse(f.read(), filename)

	with open(f'{name}.md', 'w', encoding='utf-8') as f:
		f.write(f"# {name}'s Documentation\n\n")

		for klass in (node for node in code.body if isinstance(node, ClassDef)):
			f.write(f"## {klass.name}\n")

			doc = ast.get_docstring(klass)
			if doc is not None:
				desc, *args = doc.split('\n\n')

				params = None
				attrs = None
				for i in range(len(args))[::-1]:
					if params is None and args[i].split('\n', 1)[0] == 'Parameters':
						params = args[i]
						args.pop(i)
					if attrs is None and args[i].split('\n', 1)[0] == 'Attributes':
						attrs = args[i]
						args.pop(i)

				links = {}
				for line in '\n'.join(args).split('\n'):
					match = link_regex.search(line)
					if match is not None:
						links[match.group(1)] = match.group(2)

				f.write('**' + format(desc, links) + '**\n\n')
				if params is not None:
					f.write('| Parameters | Type | Required | Description |\n')
					f.write('| :-: | :-: | :-: | :-- |\n')

					for name, t, desc in parse_params(params):
						f.write(f'| {name} | {t} | {"✕" if t.isOptional else "✔"} | {format(desc, links)} |\n')

					f.write('\n')

				if attrs is not None:
					f.write('| Attributes | Type | Can be None | Description |\n')
					f.write('| :-: | :-: | :-: | :-- |\n')
					for name, t, desc in parse_params(attrs):
						f.write(f'| {name} | {t} | {"✔" if t.isOptional else "✕"} | {format(desc, links)} |\n')

					f.write('\n')

			fun_types = (FunctionDef, AsyncFunctionDef)
			methods = [m for m in klass.body if isinstance(m, fun_types) and not m.name.startswith('__')]
			if len(methods) > 1:
				f.write('\n### Methods\n')

			for method in methods:
				name, doc = method.name, ast.get_docstring(method)
				name = name.replace("_", "\\_")

				href = f'{klass.name}.{method.name}'
				args = signature(method).replace('*', '\\*')
				coro = '_coroutine_ ' if isinstance(method, AsyncFunctionDef) else ''
				f.write(f'{coro}{klass.name}.**{name}**(_{args}_) <a id="{href}" href="#{href}">¶</a>\n>\n>')

				if doc is not None:
					*desc, params = doc.replace(' ' * 8, '\t').split('\n\n')
					params = parse_fdoc(params)
					long_desc = '\n'.join(line for line in '\n\n'.join(desc).split('\n') if line != '|coro|')
					f.write(deploy_codeblock(long_desc).replace('\n', '\n>'))

					if len(params) > 0:
						f.write('\n>\n>__Parameters:__\n')

						for name, desc in params:
							f.write(f'> * **{name}** - {desc}\n')

				f.write('\n---\n\n')


class Visitor(ast.NodeVisitor):
	def generic_visit(self, node):
		if not hasattr(node, 'parent'):
			node.parent = None

		for child in ast.iter_child_nodes(node):
			child.parent = node

		super().generic_visit(node)


def generate_events():
	with open('../aiotfm/client.py', 'r', encoding='utf-8') as f:
		code: ast.Module = ast.parse(f.read(), '../aiotfm/client.py')

	with open('Event.md', 'w', encoding='utf-8') as f:
		f.write("# Event's Documentation\n\n")

	klass = [node for node in code.body if isinstance(node, ClassDef) and node.name == 'Client'][0]
	methods = [node for node in klass.body if isinstance(node, (FunctionDef, AsyncFunctionDef))]

	Visitor().visit(code)

	for method in methods:
		for node in ast.walk(method):
			if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
				if isinstance(node.func.value, ast.Name) and node.func.attr == 'dispatch':
					# print(ast.get_source_segment(code, node))
					siblings = list(ast.iter_child_nodes(node.parent.parent))
					index = siblings.index(node.parent)
					previous = siblings[index - 1]

					while isinstance(previous, ast.AST) and 'value' in previous._fields:
						previous = previous.value

					print('dispatch', 'on_' + node.args[0].value, previous)


if __name__ == '__main__':
	# generate('../aiotfm/client.py', 'Client')
	# generate('../aiotfm/player.py', 'Player')
	# generate('../aiotfm/tribe.py', 'Tribe')
	# generate('../aiotfm/message.py', 'Message')
	# generate('../aiotfm/connection.py', 'Connection')
	# generate('../aiotfm/inventory.py', 'Inventory')
	# generate('../aiotfm/packet.py', 'Packet')
	# generate('../aiotfm/room.py', 'Room')
	# generate('../aiotfm/shop.py', 'Shop')
	# generate('../aiotfm/enums.py', 'Enums')
	# generate('../aiotfm/errors.py', 'Errors')
	generate_events()