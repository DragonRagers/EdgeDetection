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

def xGradient(img, size):
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

            """
            #gray scale comparison of pixels on corresponding sides
            for  i in range(2*size+1):
                if i < size:
                    gradient += gray(pix[x-size+i,y])
                elif i > size + 1:
                    gradient -= gray(pix[x-size+i,y])
            """

            """
            #decides whether the pixel should be white or black
            # TODO: Figure out a good cut off instead of abritary formula / number
            if int(round(gradient / (math.sqrt(255**2*3)*size) * 255)) < 17:
                color = 0
            else:
                color = 255
            """

            color = int(round(gradient * 5))
            rpix[x,y] = (color, color, color)

    return result

#creates black and white edge image, takes file name and number of pixels on each side to consider (size of pixel buffer)
def edgeDetection(name, size):
    img = Image.open(name).convert("RGB")
    xg = xGradient(img, size)
    yg = xGradient(img.rotate(90,resample=0,expand=1), size).rotate(-90,resample=0,expand=1)
    return Image.blend(xg, yg, .5)

def main():
    #command line agruments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", default = "images\\input.png")
    parser.add_argument("-p", type = int, default = 1)
    args = parser.parse_args()

    #run edge detection
    edgeDetection(args.i,args.p).show()
    print("Done")

if __name__ == "__main__":
    main()
