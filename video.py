import edge
import numpy as np
from PIL import Image
import moviepy.editor as mpy
from multiprocessing import Process, Manager, Pool

input = mpy.VideoFileClip("test.mp4")


def resize(img, basewidth = 500):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize))

def edgeFrame(t):
    return np.array(edge.edgeDetection(resize(Image.fromarray(input.get_frame(t)), 600),1,2))


#single thread approach
"""
clip = mpy.VideoClip(edgeFrame, duration=input.duration)
clip.write_gif("test.gif", fps = 1)
"""

## TODO: while this does multiprocess
if __name__ == '__main__':
    p = Pool(5)
    imgs = [p.apply(edgeFrame, args=(t,)) for t in np.linspace(0,5,10)]
    clip = mpy.ImageSequenceClip(imgs, 2)
    clip.write_gif("test.gif")
