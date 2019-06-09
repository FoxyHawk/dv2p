import frame
import sender

import cv2
import numpy

class Parser:
    def __init__(self):
        self.sender = sender.Sender(0,1)

    def run(self):
        f = frame.Frame()

        img2 = numpy.zeros((600,600,3),numpy.uint8)

        for i in range(0, 200):
            for j in range(0,600):
                img2[i][j] = (255,0,0)
        for i in range(200, 400):
            for j in range(0,600):
                img2[i][j] = (0,255,0)
        for i in range(400, 600):
            for j in range(0,600):
                img2[i][j] = (0,0,255)

        index = 0;
        while(True):
            cv2.imshow('parser',img2)

            f.from_array(index, img2)

            index += 1
            index = index % 600

            for j in range(0,600):
                img2[(000 + index)%600][j] = (255,0,0)
                img2[(200 + index)%600][j] = (0,255,0)
                img2[(400 + index)%600][j] = (0,0,255)

            self.sender.send_frame(f)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    p = Parser()
    p.run()
