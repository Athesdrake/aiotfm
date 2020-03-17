# Errors's Documentation

## AiotfmException
**Base exception class for aiotfm**

## LoginError
**Exception thrown when the login failed.**

## AlreadyConnected
**Exception thrown when the account provided is already connected.**

## IncorrectPassword
**Exception thrown when trying to connect with a wrong password.**

## InvalidEvent
**Exception thrown when you added an invalid event to the client.**

## ServerUnreachable
**Exception thrown when the Client can't connect to the server.**

## ConnectionClosed
**Exception thrown when one of the connection closes.**

## InvalidSocketData
**Exception thrown when a socket receive an invalid data.**

## EndpointError
**Exception thrown when the endpoint sends an abnormal response.**

## InternalError
**Exception thrown when the endpoint got an internal error.**

## MaintenanceError
**Exception thrown when the endpoint thinks there is a maintenance.**

## InvalidLocale
**Exception thrown when you try to load an inexistent locale.**

## PacketError
**Exception thrown when a packet encounter a problem.**

## PacketTooLarge
**Exception thrown when a packet is too large to be exported.**

## XXTEAError
**Exception thrown when the XXTEA algorithm failed.**

## XXTEAInvalidPacket
**Exception thrown when you try to cipher an empty Packet.**

## XXTEAInvalidKeys
**Exception thrown when you try to cipher a packet with an invalid key.**

## CommunityPlatformError
**Exception thrown when the community platform send an error code.**

## TradeOnWrongState
**Exception thrown when the client try an impossible action on trade due to its state.**

