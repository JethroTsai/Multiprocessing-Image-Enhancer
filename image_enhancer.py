from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir
import matplotlib.pyplot as plt
import multiprocessing
import time

class image_enhancer(multiprocessing.Process):
    def __init__(self, new_bright, new_sharp, new_contrast):
        multiprocessing.Process.__init__(self)
        self.brightness = new_bright
        self.sharpness = new_sharp
        self.contrast = new_contrast
        
    def enhance(self):
        # get image and enhance
        image = ImageEnhance.Brightness(image).enhance(self.brightness)
        image = ImageEnhance.Sharpness(image).enhance(self.sharpness)
        image = ImageEnhance.Contrast(image).enhance(self.contrast)
        
class ImageGetter(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)

def main():
    #photos_loc = input("Location of images: ")
    #edited_loc = input("Location of enhanced images: ")
    photos_loc = "photos"
    edited_loc = "edited"
    # Enhancing time in minutes
    duration = int(input("input time (in minutes): "))
    # Brightness Enhancement Factor
    new_bri= float(input("input brightness: "))
    # Sharpness Enhancement Factor
    new_sha= float (input("input sharpness: "))
    # Contrast Enhancement Factor
    new_con = float(input("input contrast: "))
    # Optional process count
    process_count = int(input("input process count: "))
    
    with multiprocessing.Manager() as manager:
        time_start = time.time()
        image_queue = multiprocessing.Queue()
        image_sem = multiprocessing.Semaphore(process_count)
        file_sem = multiprocessing.Semaphore(process_count)
        timer = time.time() + (duration * 60)
        
        flist = (listdir(photos_loc))
        file_list = manager.list(flist)
        
        print(flist)
        while (time.time() < timer):
            while(len(file_list)):
                file_sem.acquire()
                # get files
                file_sem.release()
                
                
        total_time = time.time() - time_start
        
        # write in text file
    
if __name__ == "__main__":
    main() 