from PIL import Image
import math
import argparse
"""
#averages RGB
def gray(color):
    r,g,b = color
    average = int(round((r+g+b)/3))
    return average

#converts RGB to average gray scale
def grayScale(temp):
    img = temp.copy()
    width, height = img.size
    pix = img.load()
    for x in range(width):
        for y in range(height):
            average = gray(pix[x,y])
            pix[x,y] = (average, average, average)
    return img
"""

#mean square error in RGB between 2 pixels
def colorDifference(pix1, pix2):
    r1,g1,b1 = pix1
    r2,g2,b2 = pix2
    return math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)/3

def xGradient(img, size, sensitivity):
    #gets image dimensions and loads
    width, height = img.size
    result = Image.new("RGB", (width,height),color=0)
    pix = img.load()
    rpix = result.load()

    #for all pixels at least 'size' distance from edge
    for x in range(size, width - size):
        for y in range(height):

            #difference in color between corresponding pixels on opposite sides
            gradient = 0
            for i in range(size):
                gradient += colorDifference(pix[x-size+i,y], pix[x+size-i,y])

            #scales gradient up and removes some noise
            color = int(round(gradient * 10 * sensitivity))
            if color <= 100:
                color = 0
            rpix[x,y] = (color, color, color)

    return result

#creates black and white edge image, takes file name, number of pixels to consider, and sensitivity for detection
def edgeDetection(img, size = 1, sensitivity = 1):
    xg = xGradient(img, size, sensitivity)
    yg = xGradient(img.rotate(90,resample=0,expand=1), size, sensitivity).rotate(-90,resample=0,expand=1)
    return Image.blend(xg, yg, .5)


def main():
    #command line agruments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", default = "images\\input.png")
    parser.add_argument("-p", type = int, default = 1)
    parser.add_argument("-s", type = float, default = 1)
    args = parser.parse_args()

    #run edge detection
    img = Image.open(args.i).convert("RGB")
    edgeDetection(img,args.p,args.s).show()
    print("Done")

if __name__ == "__main__":
    main()
