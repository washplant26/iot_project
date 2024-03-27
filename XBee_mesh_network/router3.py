from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import struct
import time
import serial 

def initialize_xbee(port, baud_rate=9600):
    try:
        xbee = XBeeDevice(port, baud_rate)
        xbee.open()
        return xbee
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_data(xbee, remote_device, data1, data2):
    try:
        # Convert two floats to bytes
        data_bytes = struct.pack(">ff", data1, data2)
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
    router3_port = "/dev/ttyUSB0"  # Replace with the actual port of your XBee device
    coordinator_adress = "0013A20040D8798A"

    router3 = initialize_xbee(router3_port)

    if router3 is None:
        print("Failed to initialize XBee device. Exiting.")
        return
    
    remote_coordinator = RemoteXBeeDevice(router3, XBee64BitAddress.from_hex_string(coordinator_adress))
    
    try:
        while True:
            # Receive two float values on router
            received_float_data3 = receive_data_with_counter(router3)
            time.sleep(1)
            if received_float_data3:
                print(f"Router3 received float data: {received_float_data3[0]}, {received_float_data3[1]}")
                print(f"Counter received on Router1: {received_float_data3[2]}")
                time.sleep(1)


                # Send two float values from router to coordinator
                send_data(router3, remote_coordinator, received_float_data3[0], received_float_data3[1])

            # time.sleep(10)
            # print("10 seconds")

      
        
    except serial.SerialException as e:
        print(f"SerialException: {e}")
        print("Router3 disconnected. Exiting gracefully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if router3 is not None and router3.is_open():
            router3.close()


if __name__ == "__main__":
    main()
