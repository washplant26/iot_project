from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import struct
import time

def initialize_xbee(port, baud_rate=9600):
    try:
        xbee = XBeeDevice(port, baud_rate)
        xbee.open()
        return xbee
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_data(xbee, remote_device, data1, data2,counter_value):
    try:
        # Convert two floats to bytes
        data_bytes = struct.pack(">ffI", data1, data2,counter_value)
        xbee.send_data(remote_device, data_bytes)
        print(f"Data sent from router: {data1}, {data2}")
    except Exception as e:
        print(f"Error: {e}")

def receive_data_with_counter(xbee):
    try:
        data = xbee.read_data(1000)
        if data is not None:
            # Check if data length is at least 12 bytes
            if len(data.data) >= 12:
                # Unpack bytes to two floats and a counter value (an unsigned integer)
                data_tuple = struct.unpack(">ffI", data.data[:12])  # Extract first 12 bytes for unpacking
                return data_tuple
            else:
                print("Received data packet is too short.")
    except Exception as e:
        print(f"Error: {e}")
    return None

def main():
    router1_port = "/dev/ttyUSB2"  # Replace with the actual port of your XBee device
    router2_address = "0013A20040E8E6A0"  # Replace with the actual address of the router

    router1 = initialize_xbee(router1_port)

    if router1 is None:
        print("Failed to initialize XBee device. Exiting.")
        return

    remote_router2 = RemoteXBeeDevice(router1, XBee64BitAddress.from_hex_string(router2_address))

    try:
        while True:
            # Receive data tuple (two floats and a counter) on router
            received_data = receive_data_with_counter(router1)
            time.sleep(1)
            if received_data:
                print(f"Router1 received float data: {received_data[0]}, {received_data[1]}")
                print(f"Counter received on Router1: {received_data[2]}")

                time.sleep(1)

                # Send two float values from router to coordinator
                send_data(router1, remote_router2, received_data[0], received_data[1], received_data[2])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if router1 is not None and router1.is_open():
            router1.close()

if __name__ == "__main__":
    main()
