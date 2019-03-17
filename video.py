import edge
import numpy as np
from PIL import Image
import moviepy.editor as mpy
from multiprocessing import Process, Manager, Pool

input = mpy.VideoFileClip("flower.mp4")

#resize width to input maintaining aspect ratio
def resize(img, basewidth = 500):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize))

#runs frame at time t through edge detection filter
## TODO: change edge detection to run off of numpy instead of Pillow
def edgeFrame(t):
    return np.array(edge.edgeDetection(resize(Image.fromarray(input.get_frame(t)), 600),1,2))


#single thread approach
"""
clip = mpy.VideoClip(edgeFrame, duration=input.duration)
clip.write_gif("test.gif", fps = 1)
"""

#multiprocess edge detection processing per frame and stich them back together into a gif
if __name__ == '__main__':
    time = 20
    fps = 2

    p = Pool(5)
    imgs = [p.apply(edgeFrame, args=(t,)) for t in np.linspace(0,time,time*fps)]
    clip = mpy.ImageSequenceClip(imgs, fps)
    clip.write_gif("test.gif")
