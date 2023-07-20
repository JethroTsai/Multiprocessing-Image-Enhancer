from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir
import matplotlib.pyplot as plt
import multiprocessing
import time

class image_enhancer(multiprocessing.Process):
    def __init__(self, edited_loc, new_bright, new_sharp, new_contrast, ctr, queue, remItems):
        multiprocessing.Process.__init__(self)

class main():
    photos_loc = input("Location of images: ")
    edited_loc = input("Location of enhanced images: ")
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
    
if __name__ == "__main__":
    main() 