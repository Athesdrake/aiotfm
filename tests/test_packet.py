import os
import pytest

from aiotfm import Packet
from aiotfm.errors import XXTEAInvalidKeys, XXTEAInvalidPacket


def test_constructor():
	pkt = Packet()
	assert isinstance(pkt.buffer, (bytes, bytearray))
	assert pkt.buffer == b''
	assert pkt.pos == 0

	pkt = Packet(bytes(1))
	assert isinstance(pkt.buffer, (bytes, bytearray))
	assert pkt.buffer == b'\x00'
	assert pkt.pos == 0

	pkt = Packet(bytearray(1))
	assert isinstance(pkt.buffer, (bytes, bytearray))
	assert pkt.buffer == b'\x00'
	assert pkt.pos == 0


def test_bytes():
	pkt = Packet(b'hi')
	assert bytes(pkt) == b'hi'

	pkt = Packet.new(0x4141)
	assert pkt.buffer == b'AA'


def test_new():
	pkt = Packet.new(65, 65)
	assert pkt.buffer == b'AA'

	pkt = Packet.new(0x4141)
	assert pkt.buffer == b'AA'

	pkt = Packet.new([65, 65])
	assert pkt.buffer == b'AA'


def test_copy():
	pkt = Packet(b'0123456789')
	pkt.pos = 5

	assert pkt.copy().buffer == pkt.buffer
	assert pkt.copy(True).pos == pkt.pos


def test_read():
	pkt = Packet(bytes(range(13)))

	assert pkt.read8() == 0
	assert pkt.readBool()
	assert pkt.readCode() == (2, 3)
	assert pkt.read16() == 0x0405
	assert pkt.read24() == 0x060708
	assert pkt.read32() == 0x090a0b0c

	pkt = Packet(b'\x00\x06aiotfm\x00\x06aiotfm\xde\xad\xbe\xaf')
	assert pkt.readString() == b'aiotfm'
	assert pkt.readUTF() == 'aiotfm'
	assert pkt.readBytes(4) == b'\xde\xad\xbe\xaf'


def test_write():
	pkt = Packet()
	pkt.write8(0).writeBool(True)
	pkt.writeCode(2, 3).write16(0x0405)
	pkt.write24(0x060708)
	pkt.write32(0x090a0b0c)
	assert pkt.buffer == bytes(range(13))

	pkt = Packet()
	pkt.writeString(b'aiotfm').writeUTF(b'aiotfm')
	pkt.writeBytes(b'\xde\xad\xbe\xaf')
	assert pkt.buffer == b'\x00\x06aiotfm\x00\x06aiotfm\xde\xad\xbe\xaf'

	assert Packet().write8(0x0100).buffer == bytes(1)
	assert Packet().write16(0x010000).buffer == bytes(2)
	assert Packet().write24(0x01000000).buffer == bytes(3)
	assert Packet().write32(0x0100000000).buffer == bytes(4)


def test_export():
	assert Packet(bytes(8)).export()[:2] == b'\x08\x00'
	assert Packet(bytes(256)).export(0x41)[:3] == b'\x80\x02A'


def test_xor():
	key = bytes(range(20))
	pkt = os.urandom(256)
	assert Packet(b'00aiotfm').xor_cipher(key, 0).buffer == b'00\x60klpck'
	assert Packet(pkt).xor_cipher(key, 45).xor_cipher(key, 45).buffer == pkt


def test_xxtea():
	with pytest.raises(XXTEAInvalidPacket):
		Packet(b'0').cipher([0, 1, 2])

	with pytest.raises(XXTEAInvalidKeys):
		Packet(b'00aiotfm').cipher([0, 1, 2])

	key = bytes(range(4))
	assert Packet(b'00aiotfm').cipher(key).buffer == b'00\x00\x02\xb7\xef\xee\x9en\xbf\n\xa1'
	assert Packet(b'0087654321').cipher(key).buffer == b'00\x00\x02\xd2F\x90\xb51z\x7fu'
