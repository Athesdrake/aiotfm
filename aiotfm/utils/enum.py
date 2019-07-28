class EnumMeta(type):
	base = False
	def __new__(cls, name, bases, kw):
		klass = type.__new__(cls, name, bases, kw)
		if not EnumMeta.base:
			EnumMeta.base = True
			return klass
		return klass()

class Enum(metaclass=EnumMeta):
	def __getitem__(self, key):
		if isinstance(key, int):
			for k in dir(self):
				if len(k)==2:
					if getattr(self, k)==key:
						return k
			return self.__missing__(key)
		return getattr(self, key, self.__missing__(key))

	def __missing__(self, key):
		return None

class chatCommu(Enum):
	en = 1
	fr = 2
	ru = 3
	br = 4
	es = 5
	cn = 6
	tr = 7
	vk = 8
	pl = 9
	hu = 10
	nl = 11
	ro = 12
	id = 13
	de = 14
	e2 = 15
	ar = 16
	ph = 17
	lt = 18
	jp = 19
	fi = 21
	cz = 22
	hr = 23
	bg = 25
	lv = 26
	he = 27
	it = 28
	pt = 31

	def __missing__(self, key):
		if isinstance(key, int):
			return 'int'
		return 1