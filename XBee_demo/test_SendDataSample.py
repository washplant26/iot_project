from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress

xbee = XBeeDevice("/dev/ttyUSB0", 9600)
xbee.open()

remote = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string("0013A20040DD2F5F"))
xbee.send_data(remote, "Hello XBee!")
xbee.close()