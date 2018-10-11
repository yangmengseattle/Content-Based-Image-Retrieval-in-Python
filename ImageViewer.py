# ImageViewer.py
# Program to start evaluating an image in python
#
# Show the image with:
# os.startfile(imageList[n].filename)



from tkinter import *
import math, os
from PixInfo import PixInfo

IMAGE_PATH = os.path.join(os.path.dirname(__file__).replace('/', '\\'), "images")
# Main app.
class ImageViewer(Frame):
    
    # Constructor.
    def __init__(self, master, pixInfo, resultWin):
        
        Frame.__init__(self, master)
        self.master = master
        self.pixInfo = pixInfo
        self.resultWin = resultWin
        self.colorCode = pixInfo.get_colorCode()
        self.intenCode = pixInfo.get_intenCode()
        # Full-sized images.
        self.imageList = pixInfo.get_imageList()
        # Thumbnail sized images.
        self.photoList = pixInfo.get_photoList()
        self.photoThumbList = pixInfo.getphotoThumbList()
        # Image size for formatting.
        self.xmax = pixInfo.get_xmax()
        self.ymax = pixInfo.get_ymax()
        # selected ImageID
        self.selectedImgID = 0;
        
        
        # Create Main frame.
        mainFrame = Frame(master)
        mainFrame.pack()
        
        
        # Create Picture chooser frame.
        listFrame = Frame(mainFrame)
        listFrame.pack(side=LEFT)
        
        
        # Create Control frame.
        controlFrame = Frame(mainFrame)
        controlFrame.pack(side=RIGHT)
        
        
        # Create Preview frame.
        previewFrame = Frame(mainFrame, 
            width=self.xmax+45, height=self.ymax)
        previewFrame.pack_propagate(0)
        previewFrame.pack(side=RIGHT)
        
        
        # Create Results frame.
        resultsFrame = Frame(self.resultWin)
        resultsFrame.pack(side=TOP)
        self.canvas = Canvas(resultsFrame)
        self.resultsScrollbar = Scrollbar(resultsFrame)
        self.resultsScrollbar.pack(side=RIGHT, fill=Y)
        
        '''
        # Layout Picture Listbox.
        self.listScrollbar = Scrollbar(listFrame)
        self.listScrollbar.pack(side=RIGHT, fill=Y)
        self.list = Listbox(listFrame, 
            yscrollcommand=self.listScrollbar.set, 
            selectmode=BROWSE, 
            height=10)
        for i in range(len(self.imageList)):
            self.list.insert(i, self.imageList[i].filename)
        self.list.pack(side=LEFT, fill=BOTH)
        self.list.activate(1)#?
        self.list.bind('<<ListboxSelect>>', self.update_preview)#?
        self.listScrollbar.config(command=self.list.yview)
        '''
        self.selectedImgList = []
        for i, photo in enumerate(self.photoThumbList):#the scope of i is the same with the function/block it is in
            self.selectedImgList.append(Label(listFrame,image=self.photoThumbList[i])) #appending a new label in listFrame, content is image,
            self.selectedImgList[i].grid(row=i // 10, column=i % 10)
            self.selectedImgList[i].bind('<Button-1>', lambda e, i=i: self.update_preview(e, i))#lamda: a function of one line, signature + body
        
        # Layout Controls.
        button = Button(controlFrame, text="Inspect Image",
            fg="white", bg="crimson", padx=20, width=20,
            command=lambda: self.inspect_pic(os.path.join(IMAGE_PATH, '{}.jpg'.format(self.selectedImgID+1))))
        button.grid(row=0, sticky=S)
        
        self.b1 = Button(controlFrame, text="Retrieve by Color-Code", fg="red", bg="aqua",
            padx = 20, width=20,
            command=lambda: self.find_distance(method='CC'))
        self.b1.grid(row=1, sticky=S)


        
        b2 = Button(controlFrame, text="Retrieve by Intensity", fg="red", bg="orange",
            padx = 20, width=20,
            command=lambda: self.find_distance(method='inten'))
        b2.grid(row=2, sticky=S)
        
        #self.resultLbl = Label(controlFrame, text="Results:")
        #self.resultLbl.grid(column=3, sticky=E)
        
        
        # Layout Preview.
        print(self.photoList)
        self.selectImg = Label(previewFrame, image=self.photoList[0])
        self.selectImg.pack()
    
    
    # Event "listener" for listbox change.
    def update_preview(self, event, i):
    
        # i = self.list.curselection()[0]
        self.selectImg.configure(
            image=self.photoThumbList[int(i)])
        self.selectedImgID = i
    
    
    # Find the Manhattan Distance of each image and return a
    # list of distances between image i and each image in the
    # directory uses the comparison method of the passed 
    # binList
    def find_distance(self, method):
	    #your code
        print("find_distance beginning")
        #create a distance list to hold the distances
        distanceList = [0] * len(self.imageList)

        #get the ID of selected image
        selectedID = self.selectedImgID

        #calculate the number of pixels in each image
        numOfPixels = self.imageList[selectedID].size[0] * self.imageList[selectedID].size[1]

        # initialise histogram list of different size on different method
        if method == 'inten':
            histogramSize = 25
            histogramList = self.intenCode
        elif method == 'CC':
            histogramSize = 64
            histogramList = self.colorCode
        else:
            print("method is not available")

        #distanceList = [] why?
        selectedHistogram = histogramList[selectedID]
        for i, histogram in enumerate(histogramList):
            distance = sum([abs(selectedHistogram[i] / numOfPixels - histogram[i] / numOfPixels) for i in range(histogramSize)])#numOfPixels?
            distanceList[i] = (i, distance, )
        print('Debug: selectedID =', selectedID, 'method =', method)
        print('       distanceList =', distanceList)

        #sort distance list
        sortedDistanceList = self.sortDistanceList(distanceList=distanceList)
        sortedTup = [('images/{}.jpg'.format(i+1), self.photoThumbList[i], ) for i, d in sortedDistanceList]
        self.update_results(sortedTup)

    # sorting function to return a sorted distance list, from close to farther
    def sortDistanceList(self, distanceList):
        return sorted(distanceList, key=lambda item: item[1])

    # Update the results window with the sorted results.
    def update_results(self, sortedTup):
        
        cols = int(math.ceil(math.sqrt(len(sortedTup))))
        fullsize = (0, 0, (self.xmax*cols), (self.ymax*cols))
        
        # Initialize the canvas with dimensions equal to the 
        # number of results.
        self.canvas.delete(ALL)
        self.canvas.config( 
            width=self.xmax*cols, 
            height=self.ymax*cols / 2,
            yscrollcommand=self.resultsScrollbar.set,
            scrollregion=fullsize)
        self.canvas.pack(side=RIGHT)
        self.resultsScrollbar.config(command=self.canvas.yview)
        
        # your code
        
        photoRemain = sortedTup
        # Place images on buttons, then on the canvas in order
        # by distance.  Buttons envoke the inspect_pic method.
        rowPos = 0
        while photoRemain:
            
            photoRow = photoRemain[:cols]
            photoRemain = photoRemain[cols:]
            colPos = 0
            for (filename, img) in photoRow:
                
                link = Button(self.canvas, image=img)
                handler = lambda f=filename: self.inspect_pic(f)
                link.config(command=handler)
                link.pack(side=LEFT, expand=YES)
                self.canvas.create_window(
                    colPos, 
                    rowPos, 
                    anchor=NW,
                    window=link, 
                    width=self.xmax, 
                    height=self.ymax)
                colPos += self.xmax
                
            rowPos += self.ymax
    
    
    # Open the picture with the default operating system image
    # viewer.
    def inspect_pic(self, filename):
        os.startfile(filename)


# Executable section.
if __name__ == '__main__':

    root = Tk() # a blank window
    root.title('Image Analysis Tool')

    resultWin = Toplevel(root)# create result window
    resultWin.minsize(500, 500)
    canvas = Canvas(resultWin, width=500, height=500)
    canvas.pack(side=RIGHT)#put it in the window, so that it displays
    resultWin.title('Result Viewer')
    resultWin.protocol('WM_DELETE_WINDOW', lambda: None)

    pixInfo = PixInfo(root)

    imageViewer = ImageViewer(root, pixInfo, resultWin)
    print('imageViewer')
    root.mainloop()# indefinate loop so that the window constantly display # stops here?

