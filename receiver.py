import common_network_settings as cns
import frame

import select
import socket

class Receiver:
    def __init__(self, type, num):
        self.type = type
        self.num = num

        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_data = (cns.nodes[self.type][self.num][0], cns.nodes[self.type][self.num][2])
        self.data_socket.bind(temp_data)

        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_control = (cns.nodes[self.type][self.num][0], cns.nodes[self.type][self.num][1])
        self.control_socket.bind(temp_control)
        self.control_socket.listen()

    def recv_frame(self):
        conn, addr = self.control_socket.accept()

        inputs = [conn, self.data_socket]
        with conn:
            print('Connected by', addr)
            data_control = conn.recv(cns.control_buffer_size)
            frame_id, x,y,z = frame.control_packer.unpack(data_control)

            estimated_packets = int(round(x*y*z / cns.chunk_size)) - 1

            h = {}
            conn.send('Ok'.encode())

            loop_val = True
            while loop_val:
                readable, writable, exceptional = select.select(inputs, [], inputs)

                for s in readable:
                    if s is self.data_socket:
                        data_in = self.data_socket.recv(cns.chunk_size + 100)
                        data = cns.picture_chunk_packer.unpack(data_in)
                        #print(data[0])
                        h[data[0]] = data[1:]
                        #if(data[0]==estimated_packets):
                        #    print("out loop")
                        #    loop_val = 0
                        #    break

                    if s is conn:
                        data = conn.recv(cns.control_buffer_size)
                        if data:
                            print("out loop")
                            loop_val = False
                            break

        serial_data = []
        for d in range(0, estimated_packets + 1):
            if d not in h:
                print("miss chunk {}".format(d))
                h[d] = bytearray()
                for sd in range(0, cns.chunk_size):
                    h[d].append(0)
            if d==estimated_packets:
                h[d] = h[d][0:(x*y*z) % cns.chunk_size]
            serial_data += h[d]

        f = frame.Frame()
        f.from_bytes(data_control, bytes(serial_data))
        print(f.to_string())
        return f

if __name__ == "__main__":
    r = Receiver(0, 0)
    f = r.recv_frame()
    print(f.get_control_bytes())
