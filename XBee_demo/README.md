# XBee Communication Example

This project demonstrates a simple implementation of data transmission and reception between XBee modules using the Digi XBee Python Library. The project consists of two Python scripts:

- `test_ReceiveDataSample.py`: Listens for incoming data messages from a remote XBee device.
- `test_SendDataSample.py`: Sends a data message to a remote XBee device.

## Prerequisites

Before running these scripts, ensure you have the following:

- Two XBee devices set up and connected to your computer or Raspberry Pi (one for sending data and one for receiving data).
- The Digi XBee Python Library installed. You can install it using pip:

```bash
pip install digi-xbee