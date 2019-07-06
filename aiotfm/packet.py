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
		if cc is None:
			msg.write16(c)
		else:
			msg.write8(c).write8(cc)

		return msg

	def copy(self, pos=False):
		p = Packet(self.buffer[:])
		if pos:
			p.pos = self.pos
		return p

	def unpack(self, fmt):
		fmt = '>'+fmt
		buf = self.readBytes(struct.calcsize(fmt))
		result = struct.unpack(fmt, buf)
		if len(result)==1:
			return result[0]
		return result

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
		return (self.read8() << 8) + self.read8()

	def read24(self):
		return (self.read16() << 8) + self.read8()

	def read32(self):
		return (self.read24() << 8) + self.read8()

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

	def cipher(self, keys):
		if len(self.buffer)<2:
			raise Exception()
		while len(self.buffer)<10:
			self.write8(0)

		chunks = []
		ccc = self.read16()
		length = len(self.buffer)-2
		for i in range(length//4+(length%4>0)):
			chunks.append(self.read32())

		chunks = encode_chunks(chunks, len(chunks), keys)

		packet = Packet.new(ccc).write16(len(chunks))
		for chunk in chunks:
			packet.write32(chunk)

		self.buffer = packet.buffer
		return self

def encode_chunks(v, n, keys):
	DELTA = 0x9e3779b9
	def MX():
		return int(((z>>5)^(y<<2)) + ((y>>3)^(z<<4))^(sum^y) + (keys[(p & 3)^e]^z))

	y = v[0]
	sum = 0
	if n > 1:
		z = v[n - 1]
		q = int(6 + 52 / n)
	while q > 0:
		q -= 1
		sum = (sum + DELTA) & 0xffffffff
		e = ((sum >> 2) & 0xffffffff) & 3
		p = 0
		while p < n - 1:
			y = v[p + 1]
			z = v[p] = (v[p] + MX()) & 0xffffffff
			p += 1
		y = v[0]
		z = v[n - 1] = (v[n - 1] + MX()) & 0xffffffff
	return v