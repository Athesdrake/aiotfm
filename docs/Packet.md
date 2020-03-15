# Packet's Documentation

## Packet
**Represents a network packet.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| buffer | `bytes` | ✕ |  The packet's buffer. The ``Packet`` will be read-only if given. If ``None`` is provided instead the ``Packet`` will be in write-only mode. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| buffer | `bytearray` | ✕ |  The content of the packet. |
| pos | `int` | ✕ |  The position inside the buffer. |


### Methods
@*classmethod*<br>
Packet.**new**(_cls, c, cc_) <a id="Packet.new" href="#Packet.new">¶</a>
>
>Create a new instance of Packet initialized by two bytes: c and cc.
---

Packet.**copy**(_self_) <a id="Packet.copy" href="#Packet.copy">¶</a>
>
>Returns a copy of the Packet
---

Packet.**readBytes**(_self, nbr_) <a id="Packet.readBytes" href="#Packet.readBytes">¶</a>
>
>Read raw bytes from the buffer.
---

Packet.**readCode**(_self_) <a id="Packet.readCode" href="#Packet.readCode">¶</a>
>
>Read two bytes: c and cc.
---

Packet.**read8**(_self_) <a id="Packet.read8" href="#Packet.read8">¶</a>
>
>Read a single byte from the buffer.
---

Packet.**read16**(_self_) <a id="Packet.read16" href="#Packet.read16">¶</a>
>
>Read a short (two bytes) from the buffer
---

Packet.**read24**(_self_) <a id="Packet.read24" href="#Packet.read24">¶</a>
>
>Read three bytes from the buffer
---

Packet.**read32**(_self_) <a id="Packet.read32" href="#Packet.read32">¶</a>
>
>Read an int (four bytes) from the buffer
---

Packet.**readBool**(_self_) <a id="Packet.readBool" href="#Packet.readBool">¶</a>
>
>Read a boolean (one byte) from the buffer
---

Packet.**readString**(_self_) <a id="Packet.readString" href="#Packet.readString">¶</a>
>
>return a encoded string (in bytes)
---

Packet.**readUTF**(_self_) <a id="Packet.readUTF" href="#Packet.readUTF">¶</a>
>
>return a decoded string
---

Packet.**writeBytes**(_self, content_) <a id="Packet.writeBytes" href="#Packet.writeBytes">¶</a>
>
>Write raw bytes to the buffer
---

Packet.**writeCode**(_self, c, cc_) <a id="Packet.writeCode" href="#Packet.writeCode">¶</a>
>
>Write two bytes: c and cc.
---

Packet.**write8**(_self, value_) <a id="Packet.write8" href="#Packet.write8">¶</a>
>
>Write a single byte to the buffer
---

Packet.**write16**(_self, value_) <a id="Packet.write16" href="#Packet.write16">¶</a>
>
>Write a short (two bytes) to the buffer
---

Packet.**write24**(_self, value_) <a id="Packet.write24" href="#Packet.write24">¶</a>
>
>Write three bytes to the buffer
---

Packet.**write32**(_self, value_) <a id="Packet.write32" href="#Packet.write32">¶</a>
>
>Write an int (four bytes) to the buffer
---

Packet.**writeBool**(_self, value_) <a id="Packet.writeBool" href="#Packet.writeBool">¶</a>
>
>Write a boolean (one byte) to the buffer
---

Packet.**writeString**(_self, string_) <a id="Packet.writeString" href="#Packet.writeString">¶</a>
>
>Write a string to the buffer
---

Packet.**writeUTF**(_self, string_) <a id="Packet.writeUTF" href="#Packet.writeUTF">¶</a>
>
>Write a string to the buffer. Alias for .writeString
---

Packet.**export**(_self, fp_) <a id="Packet.export" href="#Packet.export">¶</a>
>
>Generates the header then converts the whole packet to bytes and returns it.
---

Packet.**xor\_cipher**(_self, key, fp_) <a id="Packet.xor_cipher" href="#Packet.xor_cipher">¶</a>
>
>Cipher the packet with the XOR algorithm.
---

Packet.**cipher**(_self, key_) <a id="Packet.cipher" href="#Packet.cipher">¶</a>
>
>Cipher the packet with the XXTEA algorithm.
---

