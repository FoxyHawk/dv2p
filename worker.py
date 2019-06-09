import frame
import receiver
import sender

import cv2

class Worker:
    def __init__(self, num):
        self.num = num
        self.receiver = receiver.Receiver(0, num)
        self.sender = sender.Sender(1, num)

    def run(self):
        while True:
            f = self.receiver.recv_frame()
            #do stuff
            out = []

            edges = cv2.Canny(f.get_data(),100,200)
            out.append(edges)
            out.append(edges)
            out.append(edges)
            pict = cv2.merge(out)

            output = frame.Frame()
            output.from_array(f.get_index(), pict)
            self.sender.send_frame(output)

if __name__ == "__main__":
    w = Worker(1)
    w.run()
