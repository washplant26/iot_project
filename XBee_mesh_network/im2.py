from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import struct
import time
import threading

class MyCoordinator:
    def __init__(self, port, router_address):
        self.coordinator = self.initialize_xbee(port)
        self.router_address = router_address
        self.pk_sent_indicator = 0
        self.timer_duration = 5
        self.timer = threading.Timer(self.timer_duration, self.timer_callback)
        self.timeout_duration = 10
        self.data_received = False
        self.timeout_timer = threading.Timer(self.timeout_duration, self.timeout_callback)
        self.counter = 0  # Initialize counter
        self.timer.start()
        self.timeout_timer.start()
       

    def initialize_xbee(self, port, baud_rate=9600):
        try:
            xbee = XBeeDevice(port, baud_rate)
            xbee.open()
            return xbee
        except Exception as e:
            print("Error1: {e}")
            return None

    def send_data(self, data1, data2, counter_value):
        try:
            # Convert two floats to bytes
            data_bytes = struct.pack(">ffI", data1, data2, counter_value)
            remote_device = RemoteXBeeDevice(self.coordinator, XBee64BitAddress.from_hex_string(self.router_address))
            self.coordinator.send_data(remote_device, data_bytes)
            print("Data sent from coordinator: {data1}, {data2}")

            # Start the timeout timer after sending data
            #self.timeout_timer.start()
        except Exception as e:
            print("Error2: {e}")

    def receive_float_data(self):
        try:
            data = self.coordinator.read_data(1000)
            if data is not None:
                # Unpack bytes to two floats
                self.data_received = True
                return struct.unpack(">ff", data.data)
        except Exception as e:
            print("Error3: {e}")
        return None

    def increment_counter(self):
        self.counter += 1  # Increment counter value by 1

    def main_loop(self):
        try:
            #self.timer.start()
            #self.timeout_timer.start()
            # Send two float values from coordinator to router
            #float_data1 = 3.14  # Replace with your first float value
            #float_data2 = 2.71  # Replace with your second float value

            #self.pk_sent_indicator = 1
            #self.send_data(float_data1, float_data2)
           


            while True:
                # Wait for a while before receiving data
                time.sleep(1)

                # Receive two float values on coordinator
                received_float_data = self.receive_float_data()
                if received_float_data:
                    self.pk_sent_indicator = 0
                    print("coordinator received float data: {}, {}".format(received_float_data[0], received_float_data[1]))
                    self.timeout_timer.cancel()
                    # Increment counter after receiving data
                    self.increment_counter()
                    # Send data again after receiving
                    float_data1 = 3.14  # Replace with your first float value
                    float_data2 = 2.71  # Replace with your second float value
               
                    self.send_data(float_data1, float_data2, self.counter)
                    self.timeout_timer = threading.Timer(self.timeout_duration, self.timeout_callback)
                    self.timeout_timer.start()

                # Wait for a while before next round
                print("Round completed. Counter value:", self.counter)
                time.sleep(1)


               
 
     

        except Exception as e:
            print("Error4: {e}")
            import traceback
            traceback.print_exc()

        finally:
            if self.coordinator is not None and self.coordinator.is_open():
                self.coordinator.close()
            print("Exiting the script as timeout occurs")

    def timer_callback(self):
        print("Hello world")
        self.timer = threading.Timer(self.timer_duration, self.timer_callback)
        self.timer.start()

    def timeout_callback(self):
        print("Timeout: no data received")
        print("pk_sent_indicator value: {}".format(self.pk_sent_indicator))

        self.counter = 0

        
         # Send data again after timeout
        float_data1 = 3.14  # Replace with your first float value
        float_data2 = 2.71  # Replace with your second float value
        self.send_data(float_data1, float_data2, self.counter)
        self.timeout_timer = threading.Timer(self.timeout_duration, self.timeout_callback)
        self.timeout_timer.start()
       

if __name__ == "__main__":
    coordinator_port = "/dev/ttyUSB0"  # Replace with the actual port of your XBee device
    router1_address = "0013A20040D5D6AF"  # Replace with the actual address of router1

    my_coordinator = MyCoordinator(coordinator_port, router1_address)
    my_coordinator.main_loop()
