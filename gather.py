import frame
import receiver

import cv2

class Gather:
    def __init__(self):
        self.receiver = receiver.Receiver(1, 1)

    def run(self):
        while True:
            f = self.receiver.recv_frame()
            cv2.imshow('gather',f.get_data())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    g = Gather()
    g.run()
