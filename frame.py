import numpy
import struct

control_packer = struct.Struct('Q ' + 'Q Q ' + 'Q ')

class Frame:
    def __init__(self):
        self.number = 0
        self.data = numpy.zeros((0,0,3),numpy.uint8)

    def from_array(self, number, array):
        self.number = number
        self.data = array

    def from_bytes(self, control_bytes, data_bytes):
        unpacked_control = control_packer.unpack(control_bytes)
        self.number = unpacked_control[0]
        self.data = numpy.frombuffer(data_bytes, numpy.uint8)
        self.data = self.data.reshape((unpacked_control[1], unpacked_control[2], unpacked_control[3]))

    def init(self, number, x, y):
        self.number = number
        self.data = numpy.zeros((x,y,3), numpy.uint8)

    def get_control_bytes(self):
        packed_control = control_packer.pack(
            self.number,
            self.data.shape[0],
            self.data.shape[1],
            self.data.shape[2])
        return packed_control

    def get_data_bytes(self):
        return self.data.tobytes()

    def get_data(self):
        return self.data

    def get_index(self):
        return self.number

    def to_string(self):
        return "id: {} | {} {}".format(self.number, self.data.shape[0], self.data.shape[1])

if __name__ == "__main__":
    f = Frame()
    f.init(10, 10, 10)
    print (f.get_control_bytes())

    f_cp = Frame()
    f_cp.from_bytes(f.get_control_bytes(), f.get_data_bytes())
    print (f_cp.get_control_bytes())

    print(f_cp.get_data_bytes())
