import socket
import threading
import time
import struct



WINDOW_SIZE = 20
MAX_SEQ_NUMBER = 60

RECEIVE_PORT = 12345
SEND_PORT = 2077
DEST_PORT = 9092


base = 0
current_seq_number = 0
last_unsent_packet_index = 0
base_seq_number = 0





def incoming_packet_reader(packet_list):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', RECEIVE_PORT))

    while True:
        data, client_address = server_socket.recvfrom(1024)
        packet_list.append((data, client_address))

    server_socket.close()



def reliable_send(packet_list):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', SEND_PORT))
    timers = [None] * WINDOW_SIZE
    sent_packets = [None] * WINDOW_SIZE
    print("hello")
    send_thread = threading.Thread(target=send_packets, args=(server_socket, packet_list, timers, sent_packets))
    send_thread.start()




def send_packets(UDP_socket : socket.socket, packet_list : list, timers : list, sent_packets : list):
    global last_unsent_packet_index
    global base
    global current_seq_number
    
    while(True):
        #print("hello")
        if((last_unsent_packet_index < len(packet_list)) and (last_unsent_packet_index - base <  WINDOW_SIZE)):
            #data process
            data, client_address = packet_list[last_unsent_packet_index]
            processed_data = process_packet(data, current_seq_number)
            
            #send packet
            UDP_socket.sendto(processed_data, ('localhost', DEST_PORT))
            print(f"sent packet seq = {struct.unpack('<I', processed_data[0:4])[0]} base : {base_seq_number}\n")

            
            #set timer
            index = (current_seq_number - base_seq_number) % MAX_SEQ_NUMBER
            timer = threading.Timer(0.5, resend_packet, args=(UDP_socket, processed_data, client_address, index, timers))
            timer.start()
            timers[index] = timer
            sent_packets[index] = False
            
            #update indexes
            current_seq_number += 1
            current_seq_number %= MAX_SEQ_NUMBER
            last_unsent_packet_index += 1
            
        receive_ACKs(UDP_socket, timers, sent_packets)
            
            
    



def resend_packet(UDP_socket : socket.socket, packet, client_address, index, timers):
    UDP_socket.sendto(packet, ('localhost', DEST_PORT))
    seq_no = struct.unpack('<I', packet[0:4])[0]
    print(f"resent packet with seq  {struct.unpack('<I', packet[0:4])[0]}")

    timer = threading.Timer(0.5, resend_packet, args=(UDP_socket, packet, client_address, index, timers))
    timer.start()
    timers[(seq_no - base_seq_number) % MAX_SEQ_NUMBER] = timer

    




def process_packet(data, seq_number):

    # Append a 32-bit integer (in little-endian format) to the payload
    processed_data = struct.pack('<I', seq_number) + data  # Replace 42 with your desired 32-bit integer

    return processed_data






def receive_ACKs(UDP_socket : socket.socket, timers, sent_packets : list):
    global base
    global base_seq_number
    
    try:
        UDP_socket.settimeout(0.001)
        data, address = UDP_socket.recvfrom(1024)  # Adjust buffer size as needed

            # Unpack the first 32 bits (4 bytes) as an integer in little-endian format
        seq_number = struct.unpack('<I', data[0:4])[0]
            
        print(f"received ack for {seq_number}")
            
         
        index = (seq_number - base_seq_number) % MAX_SEQ_NUMBER           
                    
            
        
        sent_packets[index] = True
                        
        timers[index].cancel()
        timers[index] = None
        
        print(sent_packets)
            
        for i in range(WINDOW_SIZE):
            if sent_packets[0]:            
                if(sent_packets[0]):
                    timers.pop(0)
                    timers.append(None)
                    sent_packets.pop(0)
                    sent_packets.append((None))
                    base += 1
                    base_seq_number += 1
                    base_seq_number %= MAX_SEQ_NUMBER
                else:
                    return
            else:
                return
    
    except socket.timeout:
        return
    
    except Exception as e:
        print(e)        
            



def main():
    
    #reading all packets coming towards client and storing them into a list to be sent
    received_packets = []
    #process of reading incoming packets happens using a thread
    incoming_thread = threading.Thread(target=incoming_packet_reader, args=(received_packets,))
    incoming_thread.start()

    
    
    outgoing_thread = threading.Thread(target=reliable_send, args=(received_packets, ))
    outgoing_thread.start()

if __name__ == "__main__":
    main()
