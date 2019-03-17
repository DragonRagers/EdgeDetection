import edge
import numpy as np
from PIL import Image
import moviepy.editor as mpy
from multiprocessing import Process, Manager

input = mpy.VideoFileClip("test.mp4")


def resize(img, basewidth = 500):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize))

def edgeFrame(lock, t, list):
    lock.acquire()
    #img = edge.edgeDetection(resize(Image.fromarray(input.get_frame(t)), 600),1,2)
    #list.append(np.array(img))
    list.append(input.get_frame(t))
    lock.release()

#single thread approach
"""
clip = mpy.VideoClip(edgeFrame, duration=input.duration)
clip.write_gif("test.gif", fps = 1)
"""

## TODO: while this does multiprocess, frames end up out of order
if __name__ == '__main__':
    numProcesses = 24
    manager = Manager()
    lock = manager.Lock()
    imgList = manager.list()
    pool = []

    for n in range(numProcesses):
        pool.append(Process(target=edgeFrame, args=(lock, n/6, imgList)))
        pool[n].start()
    print("Start")
    for i in range(numProcesses):
        pool[i].join()
    print("Done")

    normalList = [img for img in imgList]
    clip = mpy.ImageSequenceClip(normalList, 3)
    clip.write_gif("test.gif")
