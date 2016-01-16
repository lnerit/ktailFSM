# using the Python Image Library (PIL) to resize an image
# works with Python27 and Python32
from PIL import Image
import os
import tkMessageBox

def resizeImage(filename,factor):
    image_file =filename#"../graph/sample.png"
    img_org = Image.open(image_file)
    # get the size of the original image
    width_org, height_org = img_org.size
    # set the resizing factor so the aspect ratio can be retained
    # factor > 1.0 increases size
    # factor < 1.0 decreases size
    factor = factor #0.75
    width = int(width_org * factor)
    height = int(height_org * factor)
    # best down-sizing filter
    img_anti = img_org.resize((width, height), Image.ANTIALIAS)
    # split image filename into name and extension
    name, ext = os.path.splitext(image_file)
    # create a new file name for saving the result
    new_image_file = "%s%s%s" % (name, str(factor), ext)
    #new_image_file = "%s%s" % (name, ext)
    img_anti.save(new_image_file)
    #print("resized file saved as %s" % new_image_file)
    
def generateNewImage():
        from PIL import Image
        my_list=[]
        img = Image.new('RGB', (255, 255))
        img.putdata(my_list)
        try:
            img.save('../graph/ktail.png')
        except IOError:
            tkMessageBox.showerror("File Error", "Error occured while saving image file")
    # one way to show the image is to activate
    # the default viewer associated with the image type
#resizeImage()
#import webbrowser
#webbrowser.open(new_image_file)