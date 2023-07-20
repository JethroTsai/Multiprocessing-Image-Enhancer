from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir
import matplotlib.pyplot as plt
import multiprocessing
import time

class image_enhancer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)

class main():
    photos_loc = input("Location of images: ")
    edited_loc = input("Location of enhanced images: ")
    # Enhancing time in minutes
    duration = int(input("input time (in minutes): "))
    # Brightness Enhancement Factor
    brightness= float(input("input brightness: "))
    # Sharpness Enhancement Factor
    sharpness= float (input("input sharpness: "))
    # Contrast Enhancement Factor
    contrast = float(input("input contrast: "))
    # Optional process count
    process_count = int(input("input process count: "))
    
    g_processes = []
    e_processes = []
    counter = 0;
    
if __name__ == "__main__":
    main() 