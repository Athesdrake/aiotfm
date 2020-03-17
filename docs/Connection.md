# Connection's Documentation

## TFMProtocol

### Methods
TFMProtocol.**data\_received**(_self, data_) <a id="TFMProtocol.data_received" href="#TFMProtocol.data_received">¶</a>
>
>
---

TFMProtocol.**connection\_made**(_self, transport_) <a id="TFMProtocol.connection_made" href="#TFMProtocol.connection_made">¶</a>
>
>
---

TFMProtocol.**connection\_lost**(_self, exc_) <a id="TFMProtocol.connection_lost" href="#TFMProtocol.connection_lost">¶</a>
>
>
---

## Connection
**Represents the connection between the client and the host.**


### Methods
Connection.**\_factory**(_self_) <a id="Connection._factory" href="#Connection._factory">¶</a>
>
>
---

_coroutine_ Connection.**connect**(_self, host, port_) <a id="Connection.connect" href="#Connection.connect">¶</a>
>
>Connect the client to the host:port
---

_coroutine_ Connection.**send**(_self, packet, cipher_) <a id="Connection.send" href="#Connection.send">¶</a>
>
>Send a packet to the socket
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md) the packet to send.
> * **cipher** - `bool` whether or not the packet should be ciphered before sending it.

---

Connection.**close**(_self_) <a id="Connection.close" href="#Connection.close">¶</a>
>
>Closes the connection.
---

Connection.**abort**(_self_) <a id="Connection.abort" href="#Connection.abort">¶</a>
>
>Abort the connection.
---

