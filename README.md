# README

## Selective Repeat Protocol Implementation

This repository contains Python code implementing a Selective Repeat protocol for reliable communication over UDP (User Datagram Protocol). The code is divided into two main components - the sender and the receiver, each running in separate threads.

### Sender Implementation (`sender.py`)

The sender side of the implementation is responsible for sending data packets over UDP to a receiver. It uses a Selective Repeat mechanism to ensure reliable delivery of packets. The key components of the sender implementation include:

1. **Packet Generation:**
   - The `process_packet` function is used to prepend a 32-bit sequence number to the payload data, creating a formatted packet.

2. **Packet Sending:**
   - The `reliable_send` function initiates the packet sending process. It creates a separate thread (`send_thread`) for sending packets and starts it.
   - The `send_packets` function continuously sends packets within the defined window size and handles timers for packet retransmission in case of timeouts.
   - Packets are sent to a specified destination port using a UDP socket.

3. **Packet Resending:**
   - The `resend_packet` function is responsible for resending a packet when a timeout occurs.

4. **Acknowledgment Handling:**
   - The `receive_ACKs` function listens for acknowledgments from the receiver and updates the sender's window accordingly.

5. **Main Function:**
   - The `main` function initializes the sender by setting up a thread for reading incoming packets (`incoming_packet_reader`) and another thread for sending packets (`reliable_send`).

### Receiver Implementation (`receiver.py`)

The receiver side of the implementation is responsible for receiving data packets, sending acknowledgments, and delivering the data to the application layer. Key components of the receiver implementation include:

1. **Packet Sequence Number Extraction:**
   - The `get_seq_number_reform_data` function extracts the sequence number from the received packet and reformats the data accordingly.

2. **Packet Receiving and Acknowledgment:**
   - The receiver uses a window to store incoming packets. It sends acknowledgments for received packets and discards out-of-order packets.
   - The receiver acknowledges each received packet by sending an acknowledgment packet to the sender.

3. **Packet Delivery:**
   - The receiver delivers in-order packets to the application layer and advances the base sequence number accordingly.

4. **Main Function:**
   - The `main` function initializes the receiver by setting up a UDP socket for receiving packets and then continuously processes incoming packets.

### Running the Code:

1. Execute the sender script (`sender.py`) in one terminal.
2. Execute the receiver script (`receiver.py`) in another terminal.
3. Run (`ncat --recv-only -u -l 54321`)
4. Run (`./lossy_link-linux 127.0.0.1:9092 127.0.0.1:7022`)
5. Run (`seq 1000 | while read; do sleep 0.01; echo "$REPLY"; done | ncat --send-only -u 127.0.0.1 12345`)



### Notes:

- The code is designed to run on the localhost, and the ports and IP addresses are set accordingly. Make sure there are no conflicts with other applications using the same ports.

- Adjustments to the code may be needed based on the specific requirements of the application or network conditions.

- This implementation provides a basic understanding of the Selective Repeat protocol and can serve as a starting point for further enhancements or integration into larger systems.
