# PixInfo.py
# Program to start evaluating an image in python

from PIL import Image, ImageTk # PIL = Python Imaging Library
import glob, os, math


# Pixel Info class.
class PixInfo:
    
    # Constructor.
    def __init__(self, master):

        print('PixInfo.init() start')
        self.master = master# what is master? Superclass?
        self.imageList = []
        self.photoList = []
        self.photoThumbList = []
        self.xmax = 0
        self.ymax = 0
        self.colorCode = []
        self.intenCode = []
        # Add each image (for evaluation) into a list,
        # and a Photo from the image (for the GUI) in a list.
        for infile in sorted(list(glob.glob('images/*.jpg')), key=lambda f: int(f.split('\\')[1].split('.')[0])):
            file, ext = os.path.splitext(infile)
            im = Image.open(infile)#array?

            # Resize the image for thumbnails.
            imSize = im.size #get an array? 2- tuple
            x = imSize[0]/4
            y = imSize[1]/4
            imResize = im.resize((int(x), int(y)), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(imResize)#resized image
            photoThumb = ImageTk.PhotoImage(imResize)
            
            print('yyyy', photo)
            # Find the max height and width of the set of pics.
            if x > self.xmax: #isn't xmax 0?
              self.xmax = x
            if y > self.ymax:
              self.ymax = y
            
            
            # Add the images to the lists.
            self.imageList.append(im)
            self.photoList.append(photo)
            self.photoThumbList.append(photoThumb)

        # Create a list of pixel data for each image and add it
        # to a list.
        for im in self.imageList[:]: # : means slicing, by default from 0 to the size of the list
            
            pixList = list(im.getdata())
            CcBins, InBins = self.encode(pixList)#color code bins, intensity bins
            self.colorCode.append(CcBins)
            self.intenCode.append(InBins)

            

    # Bin function returns an array of bins for each 
    # image, both Intensity and Color-Code methods.
    def encode(self, pixlist): #
        
        # 2D array initilazation for bins, initialized
        # to zero.
        CcBins = [0]*64
        InBins = [0]*25
        #your code

        for pix in pixlist:
            # get the colorCode
            colorCode = pix[0] // 64 * 16 + math.floor(pix[1] / 64) * 4 + math.floor(pix[2] / 64) * 1
            CcBins[colorCode] += 1
            # print("CcBins", CcBins)

            # calculate the intensity of each pixel with the given formula,
            # then put the intensity into corresponding bins
            # Note if the intensity is bigger than 250, set it to 240 so that
            # it goes to bin 24 (the bin list start from 0)
            intensity = 0.299 * pix[0] + 0.587 * pix[1] + 0.114 * pix[2]
            #print("intensity", intensity)
            if intensity >= 250:
                intensity = 240
            InBins[math.floor(intensity/10)] += 1

        # Return the list of binary digits, one digit for each
        # pixel.
        #print("InBins", InBins)
        return CcBins, InBins
    
    
    # Accessor functions:
    def get_imageList(self):
        return self.imageList
    
    def get_photoList(self):
        return self.photoList
    
    def get_xmax(self):
        return self.xmax
    
    def get_ymax(self):
        return self.ymax
    
    def get_colorCode(self):
        return self.colorCode
        
    def get_intenCode(self):
        return self.intenCode
    
    def getphotoThumbList(self):
        return self.photoThumbList
