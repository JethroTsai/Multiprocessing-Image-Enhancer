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

def image_enhancer_process(edited_loc, brightness, sharpness, contrast, image_data, counter, rem_items, stop_event):
    enhancer = ImageEnhancer(edited_loc = edited_loc, brightness=brightness, sharpness=sharpness, contrast=contrast)
    for img_data in image_data:
        if stop_event.is_set():
            break  # Exit the loop if the stop event is set
        enhancer.enhance_image(img_data)
        # locks
        with counter.get_lock():
            counter.value += 1
        with rem_items.get_lock():
            rem_items.value -= 1

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
    # Optional Process input
    process_count = int(input("input process count: "))

    t_start = time.time()
    t_end = t_start + duration * 60  # Convert duration to seconds and add to t_start
    
    image_files = [f for f in listdir(photos_loc) if os.path.isfile(os.path.join(photos_loc, f))] # Append images
    print(image_files)

    with multiprocessing.Manager() as manager:
        image_data = [(Image.open(os.path.join(photos_loc, fname)), fname) for fname in image_files]
        counter = multiprocessing.Value('i', 0)
        rem_items = multiprocessing.Value('i', len(image_files))
        chunk_size = (len(image_data) // process_count) + 1 # split for each process
        stop_event = multiprocessing.Event()
        
        processes = []
        for i in range(process_count):
            # calculate start and end index
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(image_data))
            p = multiprocessing.Process(target=image_enhancer_process,
                                        args=(edited_loc, brightness, sharpness, contrast,
                                            image_data[start_idx:end_idx], counter, rem_items, stop_event))
            processes.append(p)
            p.start()
            
            if i == process_count:
                stop_event.set()
            elif time.time() < t_end:
                time.sleep(0.1)  # Sleep for 0.1 second and check the time again
            else:
                # Time limit reached, set the stop event to signal worker processes to stop
                stop_event.set()

        # wait for processes or end time
        for p in processes:
            p.join()

    t_end = time.time()
    t_total = t_end - t_start

    with open("log_par.txt", "w") as f:
        f.write("Total Time Taken : {:.4f} \n".format(t_total))
        f.write("Number of Images Enhanced: {0} \n".format(counter.value))
        f.write("Enhanced Images Location : {0}".format(edited_loc))
        f.close()

if __name__ == "__main__":
    main()