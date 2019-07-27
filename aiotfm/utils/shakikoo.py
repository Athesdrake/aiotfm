import base64, hashlib

salt = b'\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0'

def shakikoo(string):
	"""Encrypt a password with the SHAKikoo algorithm."""
	sha256 = hashlib.sha256(string.encode()) # hash the password with SHA256
	hex256 = sha256.hexdigest().encode() # convert it into hexdecamals
	hex256 += salt # salt it

	hashed = hashlib.sha256(hex256).digest() # re-hash it
	return base64.b64encode(hashed) # return it in base64 bytes