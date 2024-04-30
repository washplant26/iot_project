from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from ascon import encrypt

xbee = XBeeDevice("/dev/ttyUSB0", 9600)
xbee.open()

message = b"This is the secret message"
key = b"your_secret_key_"
nonce = b'gggggggggggggggg'
associated_data = b""  

ciphertext = encrypt(key, nonce, associated_data, message, variant="Ascon-128")


remote = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string("0013A20040DD2F5F"))
xbee.send_data(remote, ciphertext)
xbee.close()
