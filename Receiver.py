import socket
import threading
import time
import struct


WINDOW_SIZE = 20
MAX_SEQ_NUMBER = 60

INCOMING_PORT = 7022
OUTGOING_PORT = 54321
SENDER_PORT = 9092

def get_seq_number_reform_data(data):
    seq_number = struct.unpack('<I', data[0:4])[0]
    new_data = data[1:]
    return seq_number, new_data


def main():
    receive_window = [None] * WINDOW_SIZE
    base_sequence_number = 0
    
    # Create a UDP socket for receiving packets
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.bind(('localhost', INCOMING_PORT))

    
    i = 0
    while True:
        # Receive data and address from the source port
        data, source_address = receive_socket.recvfrom(1024)

        
        seq_number , new_data = get_seq_number_reform_data(data)
        print(f"recieved seq no : {seq_number} base is : {base_sequence_number} \n")
        
        #out of window packet => send ACK
        end_index = ((WINDOW_SIZE + base_sequence_number - 1) % MAX_SEQ_NUMBER)
        if(end_index < base_sequence_number):
            if(seq_number > end_index and seq_number < base_sequence_number):
                receive_socket.sendto(data, ('localhost', SENDER_PORT))
                continue
        else:
            if(seq_number < end_index and seq_number < base_sequence_number):
                receive_socket.sendto(data, ('localhost', SENDER_PORT))
                continue
                
            if(seq_number > end_index and seq_number > base_sequence_number):
                receive_socket.sendto(data, ('localhost', SENDER_PORT))
                continue
                
            
 
        
        receive_window[((seq_number - base_sequence_number) % MAX_SEQ_NUMBER )] = (new_data, seq_number)
        #Send ACK of packet
        receive_socket.sendto(data, ('localhost', SENDER_PORT))
        print(f"Sent ack for : {seq_number} \n")

        
        
        
        
        for i in range(WINDOW_SIZE):
            if receive_window[0]:
                receive_socket.sendto(receive_window[0][0], ('localhost', OUTGOING_PORT))
                receive_window.pop(0)
                receive_window.append(None)
                base_sequence_number += 1
                base_sequence_number %= MAX_SEQ_NUMBER
            else:
                print(f"base is now : {base_sequence_number}\n")

                break
                


        
if __name__ == "__main__":
    
    main()
