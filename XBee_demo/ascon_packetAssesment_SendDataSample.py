from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.exception import TransmitException
from ascon import encrypt

xbee = XBeeDevice("/dev/ttyUSB0", 9600) 
xbee.set_sync_ops_timeout(10000)
integer_value = 3
packet_counter = 0
integer_length = len(str(integer_value))
message = b"Dude"
key = b"your_secret_key_"
nonce = b'gggggggggggggggg'
associated_data = b"" 
xbee.open()

remote = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string("0013A20040DD2F5F"))

while True:
    data_send = packet_counter.to_bytes(4, 'big') + integer_value.to_bytes(4, 'big')
    ciphertext = encrypt(key, nonce, associated_data, data_send, variant="Ascon-128")
    try:
        xbee.send_data(remote, ciphertext)
        packet_counter += 1
    except TransmitException as e:
        print("TransmitException occurred: ", e)
