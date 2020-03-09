# Packet's Documentation

## Packet
**Represents a network packet.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| buffer | `bytearray` | ✕ |  The content of the packet. |
| pos | `int` | ✕ |  The position inside the buffer. |


### Methods
Packet.**new**(_cls, c, cc_) <a id="Packet.new" href="#Packet.new">¶</a>
>
>
---

Packet.**copy**(_self_) <a id="Packet.copy" href="#Packet.copy">¶</a>
>
>
---

Packet.**readBytes**(_self, nbr_) <a id="Packet.readBytes" href="#Packet.readBytes">¶</a>
>
>
---

Packet.**readCode**(_self_) <a id="Packet.readCode" href="#Packet.readCode">¶</a>
>
>
---

Packet.**read8**(_self_) <a id="Packet.read8" href="#Packet.read8">¶</a>
>
>
---

Packet.**read16**(_self_) <a id="Packet.read16" href="#Packet.read16">¶</a>
>
>
---

Packet.**read24**(_self_) <a id="Packet.read24" href="#Packet.read24">¶</a>
>
>
---

Packet.**read32**(_self_) <a id="Packet.read32" href="#Packet.read32">¶</a>
>
>
---

Packet.**readBool**(_self_) <a id="Packet.readBool" href="#Packet.readBool">¶</a>
>
>
---

Packet.**readString**(_self_) <a id="Packet.readString" href="#Packet.readString">¶</a>
>
>
---

Packet.**readUTF**(_self_) <a id="Packet.readUTF" href="#Packet.readUTF">¶</a>
>
>
---

Packet.**writeBytes**(_self, content_) <a id="Packet.writeBytes" href="#Packet.writeBytes">¶</a>
>
>
---

Packet.**writeCode**(_self, c, cc_) <a id="Packet.writeCode" href="#Packet.writeCode">¶</a>
>
>
---

Packet.**write8**(_self, value_) <a id="Packet.write8" href="#Packet.write8">¶</a>
>
>
---

Packet.**write16**(_self, value_) <a id="Packet.write16" href="#Packet.write16">¶</a>
>
>
---

Packet.**write24**(_self, value_) <a id="Packet.write24" href="#Packet.write24">¶</a>
>
>
---

Packet.**write32**(_self, value_) <a id="Packet.write32" href="#Packet.write32">¶</a>
>
>
---

Packet.**writeBool**(_self, value_) <a id="Packet.writeBool" href="#Packet.writeBool">¶</a>
>
>
---

Packet.**writeString**(_self, string_) <a id="Packet.writeString" href="#Packet.writeString">¶</a>
>
>
---

Packet.**writeUTF**(_self, string_) <a id="Packet.writeUTF" href="#Packet.writeUTF">¶</a>
>
>
---

Packet.**export**(_self, fp_) <a id="Packet.export" href="#Packet.export">¶</a>
>
>
---

Packet.**xor\_cipher**(_self, key, fp_) <a id="Packet.xor_cipher" href="#Packet.xor_cipher">¶</a>
>
>
---

Packet.**cipher**(_self, key_) <a id="Packet.cipher" href="#Packet.cipher">¶</a>
>
>
---

