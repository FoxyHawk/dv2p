import common_network_settings as cns
import frame

import socket
from time import sleep

class Sender:
    def __init__(self, type, num):
        self.type = type
        self.num = num

    def send_frame(self, frame):
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_control = (cns.nodes[self.type][self.num][0], cns.nodes[self.type][self.num][1])
        self.control_socket.connect(temp_control)
        control_bytes = frame.get_control_bytes()
        self.control_socket.send(control_bytes)
        data = self.control_socket.recv(cns.control_buffer_size)
        #print(data)

        serialize_img = frame.get_data_bytes()
        h = []
        for x in range(0, int(round(len(serialize_img)/(cns.chunk_size)))):
            h.append(serialize_img[x*cns.chunk_size:(x+1)*cns.chunk_size])
            if((x+1)*cns.chunk_size > len(serialize_img)):
                h[x] = bytearray(h[x])
                for i in range(len(serialize_img), (x+1)*cns.chunk_size):
                    h[x].append(0)
            packet_data = cns.picture_chunk_packer.pack(x, *h[x])
            temp_data = (cns.nodes[self.type][self.num][0], cns.nodes[self.type][self.num][2])
            sent = self.data_socket.sendto(packet_data, temp_data)
            #print("{} sent".format(x))

        self.control_socket.send("ok".encode())
        self.control_socket.shutdown(1)
        self.control_socket.close()

if __name__ == "__main__":
    f = frame.Frame()
    f.init(10, 600, 600)
    print(f.get_control_bytes())

    s = Sender(0, 0)
    s.send_frame(f)
