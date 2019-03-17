import edge
import numpy as np
from PIL import Image
import moviepy.editor as mpy
from multiprocessing import Process, Lock

input = mpy.VideoFileClip("test.mp4")


def resize(img, basewidth = 500):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize))

def edgeFrame(t):
    #l.acquire()
    img = edge.edgeDetection(resize(Image.fromarray(input.get_frame(t)), 1000),1,2)
    return np.array(img)
    #l.release()

clip = mpy.VideoClip(edgeFrame, duration=input.duration)
clip.write_gif("test.gif", fps = 5)

"""
if __name__ == '__main__':
    lock = Lock()

    pool = []
    for n in range(5):
        pool.append(Process(target=edgeFrame, args=(lock, n)))
    for i in range(5):
        pool[i].start()
    print("Start")
    for i in range(5):
        pool[i].join()
    print("Done: ")
"""
