import edge
import numpy as np
from PIL import Image
import moviepy.editor as mpy
from multiprocessing import Pool

input = mpy.VideoFileClip("videos\\test.mp4")

#resize width to input maintaining aspect ratio
def resize(img, basewidth = 500):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize))

#runs frame at time t through edge detection filter
## TODO: change edge detection to run off of numpy instead of Pillow
def edgeFrame(t):
    return np.array(edge.edgeDetection(resize(Image.fromarray(input.get_frame(t)), 1000),1,1))


#single thread approach
"""
clip = mpy.VideoClip(edgeFrame, duration=input.duration)
clip.write_gif("test.gif", fps = 1)
"""

#multiprocess edge detection processing per frame and stich them back together into a gif
if __name__ == '__main__':
    time = 5
    fps = 24

    p = Pool(8)
    results = [p.apply_async(edgeFrame, args=(t,)) for t in np.linspace(0,time,time*fps)]
    imgs = [p.get() for p in results]
    clip = mpy.ImageSequenceClip(imgs, fps)
    clip.write_gif("pew.gif")
