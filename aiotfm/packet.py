from aiotfm.errors import PacketError, PacketTooLarge, XXTEAInvalidPacket, XXTEAInvalidKeys

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
		self._fp = 0

	def __repr__(self):
		return '<Packet {!r}>'.format(bytes(self))

	def __bytes__(self):
		return bytes(self.buffer)

	@classmethod
	def new(cls, c, cc=None):
		"""Create a new instance of Packet initialized by two bytes: c and cc."""
		msg = cls()
		if isinstance(c, (tuple, list)):
			c, cc = c
		if cc is None:
			return msg.write16(c)
		return msg.write8(c).write8(cc)

	def copy(self, pos=False):
		"""Returns a copy of the Packet"""
		p = Packet(self.buffer.copy())
		if pos:
			p.pos = self.pos
		return p

	def readBytes(self, nbr=1):
		"""Read raw bytes from the buffer."""
		self.pos += nbr
		return self.buffer[self.pos-nbr:self.pos]

	def readCode(self):
		"""Read two bytes: c and cc."""
		return self.read8(), self.read8()

	def read8(self):
		"""Read a single byte from the buffer."""
		self.pos += 1
		return self.buffer[self.pos-1]

	def read16(self):
		"""Read a short (two bytes) from the buffer"""
		return struct.unpack('>H', self.readBytes(2))[0]

	def read24(self):
		"""Read three bytes from the buffer"""
		return int.from_bytes(self.readBytes(3), 'big')

	def read32(self):
		"""Read an int (four bytes) from the buffer"""
		return struct.unpack('>I', self.readBytes(4))[0]

	def readBool(self):
		"""Read a boolean (one byte) from the buffer"""
		return self.read8() == 1

	def readString(self):
		"""return a encoded string (in bytes)"""
		return bytes(self.readBytes(self.read16()))

	def readUTF(self):
		"""return a decoded string"""
		return self.readString().decode()

	def writeBytes(self, bytes):
		"""Write raw bytes to the buffer"""
		if isinstance(bytes, Packet):
			self.buffer.extend(bytes.buffer)
		else:
			self.buffer.extend(bytes)
		return self

	def writeCode(self, c, cc):
		"""Write two bytes: c and cc."""
		return self.write8(c).write8(cc)

	def write8(self, value):
		"""Write a single byte to the buffer"""
		self.buffer.append(value & 0xff)
		return self

	def write16(self, value):
		"""Write a short (two bytes) to the buffer"""
		self.buffer.extend(struct.pack('>H', value & 0xffff))
		return self

	def write24(self, value):
		"""Write three bytes to the buffer"""
		self.buffer.extend((value & 0xffffff).to_bytes(3, 'big'))
		return self

	def write32(self, value):
		"""Write an int (four bytes) to the buffer"""
		self.buffer.extend(struct.pack('>I', value & 0xffffffff))
		return self

	def writeBool(self, value):
		"""Write a boolean (one byte) to the buffer"""
		return self.write8(1 if value else 0)

	def writeString(self, string):
		"""Write a string to the buffer"""
		if isinstance(string, str):
			string = string.encode()
		return self.write16(len(string)).writeBytes(string)

	def writeUTF(self, string):
		"""Write a string to the buffer. Alias for .writeString"""
		return self.writeString(string)

	def export(self, fp=0):
		"""Generates the header then converts the whole packet to bytes and returns it."""
		if self.exported and self._fp == fp:
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
			raise PacketTooLarge("The Packet maximum size of 16777215 has been exceeded.")
		m.write8(fp)

		self.bytes = bytes(m.buffer + self.buffer)
		self.exported = True
		self._fp = fp

		return self.bytes

	def xor_cipher(self, key, fp):
		"""Cipher the packet with the XOR algorithm."""
		fp += 1
		ccc = self.readBytes(2)
		tmp = bytearray([(byte^key[(fp+i)%20])&0xff for i, byte in enumerate(self.buffer[2:])])
		self.buffer = ccc+tmp
		return self

	def cipher(self, key):
		"""Cipher the packet with the XXTEA algorithm."""
		if len(self.buffer)<2:
			raise XXTEAInvalidPacket("The Packet is empty.")
		if len(key)<4:
			raise XXTEAInvalidKeys(str(key))

		ccc = self.read16()
		length = len(self.buffer)-2
		if length % 4 > 0:
			self.buffer.extend(bytes(4 - length % 4))

		chunks = struct.unpack(f'>{length//4}I', self.readBytes(length))
		chunks = xxtea_encode(list(chunks), len(chunks), key)

		packet = Packet.new(ccc).write16(len(chunks))
		packet.writeBytes(struct.pack(f'>{len(chunks)}I', *chunks))

		self.buffer = packet.buffer
		return self

DELTA = 0x9e3779b9

def xxtea_encode(v, n, key):
	"""https://en.wikipedia.org/wiki/XXTEA"""
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