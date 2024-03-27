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

def send_data(xbee, remote_device, data1, data2, counter_value):
    try:
        # Convert two floats and a counter value to bytes
        data_bytes = struct.pack(">ffI", data1, data2, counter_value)
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
    router2_port = "/dev/ttyUSB1"  # Replace with the actual port of your XBee device
    router3_address = "0013A20040D5D3D7"  # Replace with the actual address of the router

    router2 = initialize_xbee(router2_port)

    if router2 is None:
        print("Failed to initialize XBee device. Exiting.")
        return

    remote_router3 = RemoteXBeeDevice(router2, XBee64BitAddress.from_hex_string(router3_address))

    try:
        while True:
            # Receive data tuple (two floats and a counter) on router
            received_data = receive_data_with_counter(router2)
            time.sleep(1)
            if received_data:
                print(f"Router2 received float data: {received_data[0]}, {received_data[1]}")
                print(f"Counter received on Router2: {received_data[2]}")
            
                time.sleep(1)

                # Send two float values from router to coordinator
                send_data(router2, remote_router3, received_data[0], received_data[1],received_data[2])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if router2 is not None and router2.is_open():
            router2.close()

if __name__ == "__main__":
    main()
