# XBee Communication Network

This project demonstrates a basic setup for creating a communication network using XBee devices. It includes a Python script for the coordinator (`im2.py`) and three router scripts (`r.py`, `router2.py`, `router3.py`). These scripts facilitate the sending and receiving of data between XBee devices in a coordinated network. The network is designed to transmit float data and a counter value across devices to showcase basic XBee communication capabilities.

## Getting Started

### Prerequisites

- Python 3.x
- XBee Python library: `digi-xbee`
- Serial port access to connect XBee devices

### Installation

1. Install the XBee Python library:
   ```sh
   pip install digi-xbee
