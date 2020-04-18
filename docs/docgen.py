import ast
import glob
import re

from ast import ClassDef, FunctionDef, AsyncFunctionDef
from tokenize import generate_tokens, COMMENT


link_regex = re.compile(r'^\.{2}\s*_([^:]+):\s*(https?://(?:\w+\.)+\w+(?:/[.\w-]*)*)')
link_ref_regex = re.compile(r'`([^`]+)`_')
params_regex = re.compile(r'\n([^:\n]+):\s*([^\n]+)((?:\n\s+(?:[^\n]+))+)')
params_doc_regex = re.compile(r':param (\w+): (.+)')
return_doc_regex = re.compile(r':return: (.+)')
type_regex_op = re.compile(r'(?:(Optional)\[)?(?::(class|meth):`)?([^`]+)(?(2)`)(?(1)\])')
type_regex = re.compile(r':(class|meth):`([^`]+)`')
codeblock_regex = re.compile(r'\n([\w ]+): ::((?:\n+\t[^\n]+)+)')
event_regex = re.compile(r'^:([^:]+): (.+)$')


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

			return f'[`{name}`]({link}{anchor})'

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

	match = return_doc_regex.search(doc)
	returns = match.group(1) if match is not None else None

	return params, returns


def format(string, links):
	def repl_types(m):
		type_, name = m.groups()
		if name in dir(__builtins__):
			return f'`{name}`'

		link = name.replace(' ', '-')
		name = name.split('.')[-1]
		parts = link.split('.')

		if type_ == 'meth':
			if parts[0] == 'aiotfm':
				anchor = '.'.join(parts[1:])
				return f'[`{name}`]({parts[1].title()}.md#{anchor})'
			return f'[`{name}`](#{link})'

		if len(parts) > 1 and parts[0] == 'aiotfm':
			parts[1] = parts[1].title()
			link = f'{parts[1]}.md'
			anchor = ".".join(parts[2:])
			if len(anchor) > 0:
				anchor = '#' + anchor

			return f'[`{name}`]({link}{anchor})'

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


def generate(filename, doc_name):
	tree = []

	with open(filename, 'r', encoding='utf-8') as f:
		code: ast.Module = ast.parse(f.read(), filename)

	with open(f'{doc_name}.md', 'w', encoding='utf-8') as f:
		f.write(f"# {doc_name}'s Documentation\n\n")

		for klass in (node for node in code.body if isinstance(node, ClassDef)):
			tree.append(klass.name)
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

				decorators = [node.id for node in method.decorator_list]
				if 'property' not in decorators:
					tree.append('.'.join((klass.name, method.name)))

				for deco in decorators:
					f.write(f'@*{deco}*<br>\n')
				f.write(f'{coro}{klass.name}.**{name}**(_{args}_) <a id="{href}" href="#{href}">¶</a>\n>\n>')

				if doc is not None:
					parts = doc.replace(' ' * 8, '\t').split('\n')
					parts.append('')

					for i, part in enumerate(parts):
						if part.strip().startswith(':'):
							break

					params, returns = parse_fdoc('\n'.join(parts[i:]))
					desc = '\n'.join(line for line in parts[:i] if line != '|coro|').strip('\n')
					f.write(deploy_codeblock(format(desc, {})).replace('\n', '\n>'))

					if len(params) > 0:
						f.write('\n>\n>__Parameters:__\n')

						for name, desc in params:
							f.write(f'> * **{name}** - {format(desc, {})}\n')

						if returns is not None:
							returns = format(returns, {})
							f.write(f'>\n>__Returns:__ {returns}\n')

				f.write('\n---\n\n')

	return tree


class EventDoc:
	def __init__(self, name, node):
		self.name = name
		self.node = node
		self.default = True
		self.doc = []

	@staticmethod
	def dump(node):
		dump = EventDoc.dump

		if isinstance(node, ast.Name):
			return node.id

		if isinstance(node, ast.Constant):
			return repr(node.value)

		if isinstance(node, ast.Attribute):
			return f'{dump(node.value)}.{node.attr}'

		if isinstance(node, ast.Call):
			args = [dump(arg) for arg in node.args]
			args.extend(f'{kw.arg}={dump(kw.value)}' for kw in node.keywords)
			return f'{dump(node.func)}({", ".join(args)})'

		if isinstance(node, ast.Subscript):
			return f'{dump(node.value)}[{dump(node.slice)}]'

		if isinstance(node, ast.Index):
			return dump(node.value)

		if isinstance(node, ast.Starred):
			return f'*{dump(node.value)}'

		if isinstance(node, ast.BinOp):
			return ' '.join(dump(getattr(node, field)) for field in node._fields)

		if isinstance(node, ast.Sub):
			return '-'

		if isinstance(node, ast.Mult):
			return '*'

		raise f"Cannot dump {node.__class__.__name__}"

	def generate_default(self):
		args = [self.dump(arg) for arg in self.node.args[1:]]
		sargs = ", ".join(args)
		if len(sargs) > 0:
			sargs = f'_{sargs}_'

		self.default = True
		self.doc = [f'## on_{self.name}({sargs})']

		if len(args) > 0:
			self.doc.append('>__Parameters:__')
			self.doc.extend((f'> * **{arg}**' for arg in args))

	def generate(self, doc):
		self.default = False

		desc, args = '', []
		for line in doc:
			name, text = event_regex.match(line).groups()

			if name == 'desc':
				desc = text
			else:
				args.append((name.split()[1].replace('*', '\\*'), text))

		sargs = ', '.join(arg[0] for arg in args)
		if len(sargs) > 0:
			sargs = f'_{sargs}_'

		self.doc = [
			f'## on_{self.name}({sargs})',
			desc
		]

		if len(args) > 0:
			self.doc.append('>__Parameters:__')
			self.doc.extend(f'> * **{name}** - {desc}' for name, desc in args)


class Visitor(ast.NodeVisitor):
	def __init__(self, code, comments):
		self.lineno = 0
		self.events = {}
		self.comments = comments
		self.doc = []

	def generic_visit(self, node):
		if not hasattr(node, 'parent'):
			node.parent = None

		for child in ast.iter_child_nodes(node):
			child.parent = node

		super().generic_visit(node)

	def visit_Call(self, node):
		if not isinstance(node.func, ast.Attribute) or node.func.attr != 'dispatch':
			return

		doc = []
		evt = node.args[0].value

		if self.lineno > node.lineno:
			self.lineno = node.parent.parent.lineno

		for i in range(node.lineno - 1, max(self.lineno, node.parent.parent.lineno - 1), -1):
			if i not in self.comments:
				continue

			doc.append(self.comments[i][1:].strip())

			if ':desc:' in self.comments[i]:
				break

		while len(doc) and not doc[-1].startswith(':'):
			doc.pop()

		for i in range(len(doc) - 1, 0, -1):
			if not doc[i].startswith(':'):
				doc[i] = f'{doc.pop(i + 1)} {doc[i]}'

		event_doc = EventDoc(evt, node)
		self.lineno = node.lineno
		if len(doc) > 0:
			if evt in self.events and not self.events[evt].default:
				raise f"duplicate documentation for on_{evt}."

			event_doc.generate(doc[::-1])
		elif evt not in self.events:
			event_doc.generate_default()
		else:
			return

		self.events[evt] = event_doc


def generate_events():
	with open('Events.md', 'w', encoding='utf-8') as f:
		f.write("# Events' Documentation\n\n")

		events = {}
		for file in glob.iglob('../aiotfm/**', recursive=True):
			if not file.endswith('.py'):
				continue

			with open(file, 'r', encoding='utf-8') as f2:
				comments = {t.start[0]: t.string for t in generate_tokens(f2.readline) if t.type == COMMENT}
				f2.seek(0)
				code: ast.Module = ast.parse(f2.read(), '../aiotfm/client.py')

				visitor = Visitor(code, comments)
				visitor.visit(code)

				for evt, doc in visitor.events.items():
					if evt in events:
						if doc.default:
							visitor.events[evt] = events[evt]
						elif events[evt].default:
							pass
						else:
							raise f"duplicate documentation for on_{evt}."

				events.update(visitor.events)

		for event in events.values():
			f.write(format('\n'.join(event.doc), {}))
			f.write('\n\n---\n\n')


def generate_readme(files):
	with open('README.md', 'w', encoding='utf-8') as f:
		f.write('# Documentation\nYou can find here all documentation on `aiotfm`.\n\n')
		f.write("## API Reference\n")

		for file, tree in files.items():
			f.write(f'* [{file}.md]({file}.md)\n')
			for name in tree:
				display_name = name.replace('_', '\\_')
				tab = '  ' * name.count('.')

				f.write(f' {tab} * [{display_name}]({file}.md#{name})\n')


if __name__ == '__main__':
	files = [
		'Client', 'Player', 'Tribe', 'Message', 'Connection',
		'Inventory', 'Packet', 'Room', 'Shop', 'Enums', 'Errors'
	]
	tree = {}

	for file in files:
		tree[file] = generate(f'../aiotfm/{file.lower()}.py', file)

	generate_readme(tree)
	generate_events()