import edge
import numpy as np
from PIL import Image
import moviepy.editor as mpy
from multiprocessing import Pool
from tqdm import tqdm
from scipy import ndimage

input = mpy.VideoFileClip("videos\\flower.mp4")

#resize width to input maintaining aspect ratio
def resize(img, basewidth = 500):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize))

"""
#runs frame at time t through edge detection filter
## TODO: change edge detection to run off of numpy instead of Pillow
def edgeFrame(t):
    return np.array(edge.edgeDetection(resize(Image.fromarray(input.get_frame(t)), 1080),1,1))
    #return np.array(edge.edgeDetection(Image.fromarray(input.get_frame(t)),1,1))
"""

#single thread approach
"""
clip = mpy.VideoClip(edgeFrame, duration=input.duration)
clip.write_gif("test.gif", fps = 1)
"""

def edgeFrame(t):
    #take frame a time = t and convert to gray scale
    img = input.get_frame(t).dot([.07, .72, .21])

    #sobel filter
    dx = ndimage.sobel(img, 0)  # horizontal derivative
    dy = ndimage.sobel(img, 1)  # vertical derivative
    mag = np.hypot(dx, dy).astype(np.uint8)
    #I don't know why i need to do this
    return np.array(Image.fromarray(mag).convert("RGB"))


#multiprocess edge detection processing per frame and stich them back together into a gif
if __name__ == '__main__':
    time = round(input.duration)
    fps = 24

    print("Applying Edge Detection Algorithm to Frames:")
    p = Pool(8)
    imgs = list(tqdm(p.imap(edgeFrame, np.linspace(0,time,time*fps)), total=time*fps))

    clip = mpy.ImageSequenceClip(imgs, fps)
    clip.write_videofile("test.mp4")
    #clip.write_gif("test.gif")
    print("Done :)")
