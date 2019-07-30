import struct

class Packet:
	def __init__(self, buffer=None):
		if buffer is None:
			buffer = bytearray()
		elif not isinstance(buffer, bytearray):
			buffer = bytearray(buffer)

		self.buffer = buffer
		self.pos = 0

		self.exported = False

	def __repr__(self):
		return '<Packet {!r}>'.format(bytes(self))

	def __bytes__(self):
		return bytes(self.buffer)

	@classmethod
	def new(cls, c, cc=None):
		msg = cls()
		if isinstance(c, (tuple, list)):
			c, cc = c
		if cc is None:
			return msg.write16(c)
		return msg.write8(c).write8(cc)

	def copy(self, pos=False):
		p = Packet(self.buffer[:])
		if pos:
			p.pos = self.pos
		return p

	def readBytes(self, nbr=1):
		self.pos += nbr
		return self.buffer[self.pos-nbr:self.pos]

	def readCode(self):
		return self.read8(), self.read8()

	def read8(self):
		self.pos += 1
		try:
			return self.buffer[self.pos-1]
		except:
			return 0

	def read16(self):
		return (self.read8() << 8) | self.read8()

	def read24(self):
		return (self.read16() << 8) | self.read8()

	def read32(self):
		return (self.read24() << 8) | self.read8()

	def readBool(self):
		return self.read8()==1

	def readString(self):
		"""return a encoded string (in bytes)"""
		return bytes(self.readBytes(self.read16()))

	def readUTF(self):
		"""return a decoded string"""
		return self.readString().decode()

	def writeBytes(self, bytes):
		if isinstance(bytes, Packet):
			self.buffer.extend(bytes.buffer)
		else:
			self.buffer.extend(bytes)
		return self

	def writeCode(self, c, cc):
		return self.write8(c).write8(cc)

	def write8(self, value):
		self.buffer.append(value&0xff)
		return self

	def write16(self, value):
		return self.write8(value>>8).write8(value)

	def write24(self, value):
		return self.write16(value>>8).write8(value)

	def write32(self, value):
		return self.write24(value>>8).write8(value)

	def writeBool(self, value):
		return self.write8(1 if value else 0)

	def writeString(self, string):
		if isinstance(string, str):
			string = string.encode()
		return self.write16(len(string)).writeBytes(string)

	def export(self, fp=0):
		if self.exported:
			return self.bytes

		m = Packet()
		size = len(self.buffer)
		if size<=0xff:
			m.write8(1).write8(size)
		elif size<=0xffff:
			m.write8(2).write16(size)
		elif size<=0xffffff:
			m.write8(3).write24(size)
		else:
			raise Exception('Packet too long')
		m.write8(fp)

		self.bytes = bytes(m.buffer + self.buffer)
		self.exported = True

		return self.bytes

	def xor_cipher(self, keys, fp):
		fp += 1
		ccc = self.readBytes(2)
		tmp = bytearray([(byte^keys[(fp+i)%20])&0xff for i, byte in enumerate(self.buffer[2:])])
		self.buffer = ccc+tmp
		return self

	def cipher(self, key):
		if len(self.buffer)<2:
			raise Exception()
		while len(self.buffer)<10:
			self.write8(0)

		chunks = []
		ccc = self.read16()
		length = len(self.buffer)-2
		for i in range(length//4+(length%4>0)):
			chunks.append(self.read32())

		chunks = xxtea_encode(chunks, len(chunks), key)

		packet = Packet.new(ccc).write16(len(chunks))
		for chunk in chunks:
			packet.write32(chunk)

		self.buffer = packet.buffer
		return self

DELTA = 0X9E3779B9

def xxtea_encode(v, n, key):
	cycles = 6 + 52//n
	sum = 0
	z = v[-1]
	for _ in range(cycles):
		sum = (sum + DELTA) & 0xffffffff
		e = sum >> 2 & 3
		for p in range(n):
			y = v[(p+1)%n]
			z = v[p] = (v[p] + (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z))))&0xffffffff
	return v