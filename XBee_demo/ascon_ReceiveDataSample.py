from digi.xbee.devices import XBeeDevice
from ascon import decrypt

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    message_count = 0
    key = b"your_secret_key_"
    nonce = b'gggggggggggggggg'
    associated_data = b""  

    try:
        device.open()

        def data_receive_callback(xbee_message):
            nonlocal message_count
            message_count += 1
            # print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(), xbee_message.data.decode()))
            # ~ the_message = xbee_message.data.decode('latin-1')
            the_message = xbee_message.data
            decrypted_message = decrypt(key, nonce, associated_data, the_message, variant="Ascon-128")
            decrypted_message_str = decrypted_message.decode()
            print(f"Message #{message_count}: From {xbee_message.remote_device.get_64bit_addr()} >> {decrypted_message_str}")

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
