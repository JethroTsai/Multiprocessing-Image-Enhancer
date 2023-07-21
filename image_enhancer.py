from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir
import time
import multiprocessing

class ImageEnhancer:
    def __init__(self, edited_loc, brightness, sharpness, contrast):
        self.edited_loc = edited_loc
        self.brightness = brightness
        self.sharpness = sharpness
        self.contrast = contrast

    def enhance_image(self, img_data):
        imgage, imgage_name = img_data
        imgage = ImageEnhance.Brightness(imgage).enhance(self.brightness)
        imgage = ImageEnhance.Sharpness(imgage).enhance(self.sharpness)
        imgage = ImageEnhance.Contrast(imgage).enhance(self.contrast)
        imgage.save(os.path.join(self.edited_loc, imgage_name), "JPEG")
        imgage.show()

def image_enhancer_process(edited_loc, brightness, sharpness, contrast, image_data, counter, remaining_items):
    enhancer = ImageEnhancer(edited_loc = edited_loc, brightness=brightness, sharpness=sharpness, contrast=contrast)
    for img_data in image_data:
        enhancer.enhance_image(img_data)
        # locks
        with counter.get_lock():
            counter.value += 1
        with remaining_items.get_lock():
            remaining_items.value -= 1

def main():
    photos_loc = input("Location of Images: ")
    edited_loc = input("Location of Enhanced Images: ")
    # Enhancing time in units
    duration = int(input("input time: "))
    # Brightness
    brightness = float(input("input brightness: "))
    # Sharpness
    sharpness = float(input("input sharpness: "))
    # Contrast
    contrast = float(input("input contrast: "))
    process_count = int(input("input process count: "))

    t_start = time.time()
    # append images
    image_files = [f for f in listdir(photos_loc) if os.path.isfile(os.path.join(photos_loc, f))]
    print(image_files)

    with multiprocessing.Manager() as manager:
        image_data = [(Image.open(os.path.join(photos_loc, fname)), fname) for fname in image_files]
        counter = multiprocessing.Value('i', 0)
        remaining_items = multiprocessing.Value('i', len(image_files))
        # split for each process
        chunk_size = (len(image_data) // process_count) + 1

        processes = []
        for i in range(process_count):
            # calculate start and end index
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(image_data))
            p = multiprocessing.Process(target=image_enhancer_process,
                                        args=(edited_loc, brightness, sharpness, contrast,
                                              image_data[start_idx:end_idx], counter, remaining_items))
            processes.append(p)
            p.start()

        # wait for processes
        for p in processes:
            p.join()

    t_end = time.time()
    t_total = t_end - t_start

if __name__ == "__main__":
    main()