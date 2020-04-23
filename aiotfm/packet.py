import struct

from aiotfm.errors import XXTEAInvalidPacket, XXTEAInvalidKeys


class Packet:
	"""Represents a network packet.

	Parameters
	----------
	buffer: Optional[:class:`bytes`]
		The packet's buffer. The :class:`Packet` will be read-only if given.
		If ``None`` is provided instead the :class:`Packet` will be in write-only mode.

	Attributes
	----------
	buffer: :class:`bytearray`
		The content of the packet.
	pos: :class:`int`
		The position inside the buffer.
	"""
	def __init__(self, buffer=None):
		if buffer is None:
			buffer = bytearray()
		elif not isinstance(buffer, bytearray):
			buffer = bytearray(buffer)

		self.buffer = buffer
		self.pos = 0

	def __repr__(self):
		return '<Packet {!r}>'.format(bytes(self))

	def __bytes__(self):
		return bytes(self.buffer)

	@classmethod
	def new(cls, c, cc=None):
		"""Create a new instance of Packet initialized by two bytes: c and cc."""
		if isinstance(c, (tuple, list)):
			c, cc = c
		elif cc is None:
			return cls().write16(c)

		return cls().write8(c).write8(cc)

	def copy(self, copy_pos=False):
		"""Returns a copy of the Packet"""
		p = Packet()
		if copy_pos:
			p.pos = self.pos

		p.buffer = self.buffer.copy()
		return p

	def readBytes(self, nbr=1):
		"""Read raw bytes from the buffer."""
		self.pos += nbr
		return self.buffer[self.pos - nbr:self.pos]

	def readCode(self):
		"""Read two bytes: c and cc."""
		return self.read8(), self.read8()

	def read8(self):
		"""Read a single byte from the buffer."""
		self.pos += 1
		return self.buffer[self.pos - 1]

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

	def writeBytes(self, content):
		"""Write raw bytes to the buffer"""
		if isinstance(content, Packet):
			self.buffer.extend(content.buffer)
		else:
			self.buffer.extend(content)
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
		m = Packet()
		size = len(self.buffer)
		size_type = size >> 7
		while size_type != 0:
			m.write8(size & 0x7f | 0x80)
			size = size_type
			size_type >>= 7
		m.write8(size & 0x7f)
		m.write8(fp)

		return bytes(m.buffer + self.buffer)

	def xor_cipher(self, key, fp):
		"""Cipher the packet with the XOR algorithm."""
		self.buffer[2:] = (byte ^ key[i % 20] for i, byte in enumerate(self.buffer[2:], fp + 1))
		return self

	def cipher(self, key):
		"""Cipher the packet with the XXTEA algorithm."""
		if len(self.buffer) < 2:
			raise XXTEAInvalidPacket("The Packet is empty.")
		if len(key) < 4:
			raise XXTEAInvalidKeys(str(key))

		header = self.buffer[:2]
		length = len(self.buffer) - 2
		if length % 4 > 0:
			pad = 4 - length % 4
			self.buffer.extend(bytes(pad))
			length += pad

		chunks = struct.unpack(f'>{length//4}I', self.buffer[2:])
		chunks = xxtea_encode(list(chunks), len(chunks), key)

		packet = Packet(header).write16(len(chunks))
		packet.writeBytes(struct.pack(f'>{len(chunks)}I', *chunks))

		self.buffer = packet.buffer
		return self


DELTA = 0x9e3779b9


def xxtea_encode(v, n, key):
	"""https://en.wikipedia.org/wiki/XXTEA"""
	cycles = 6 + 52 // n
	sum_ = 0
	z = v[-1]
	for _ in range(cycles):
		sum_ = (sum_ + DELTA) & 0xffffffff
		e = sum_ >> 2 & 3
		for p in range(n):
			y = v[(p + 1) % n]
			z = v[p] = (v[p] + (
				((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum_ ^ y) + (key[(p & 3) ^ e] ^ z))
			)) & 0xffffffff
	return v