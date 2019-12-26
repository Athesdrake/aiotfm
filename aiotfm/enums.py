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

class commu(Enum):
	en = 0
	fr = 1
	br = 2
	es = 3
	cn = 4
	tr = 5
	vk = 6
	pl = 7
	hu = 8
	nl = 9
	ro = 10
	id = 11
	de = 12
	e2 = 13
	ar = 14
	ph = 15
	lt = 16
	jp = 17
	ch = 18
	fi = 19
	cz = 20
	sk = 21
	hr = 22
	bu = 23
	lv = 24
	he = 25
	it = 26
	et = 27
	az = 28
	pt = 29

	def __missing__(self, key):
		if isinstance(key, int):
			return 'int'
		return 0


class TradeState(Enum):
	ON_INVITE = 0
	ACCEPTING = 1
	TRADING = 2
	CANCELLED = 3
	SUCCESS = 4


class TradeError(Enum):
	ALREADY_TRADING = 0
	INVITE_DECLINED = 1
	CANCELLED = 2
	SAME_ROOM = 3
	SUCCEED = 4
	SHAMAN = 5
	NOT_CONNECTED = 6
	INTERNAL = 7