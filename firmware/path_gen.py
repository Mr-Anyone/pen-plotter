import cv2 as cv
import matplotlib.pyplot as plt 
import numpy as np 
from compress import compress_paths
from export_file_template import write_to_file
import requests

def get_image_from_internet(url, filename='internet.png'):
    with open(filename, "wb") as f:
        f.write(requests.get(url).content) 

    return filename
    
def get_contours(path_to_image):
    image = cv.imread(path_to_image)
    if image is None: 
        print("Cannot read image")
        exit(-1)
    
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    image = cv.flip(image, cv.ROTATE_90_CLOCKWISE)
    
    ret, thres = cv.threshold(image, 170, 255, 0)
    contours, hierarchy = cv.findContours(thres, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    return contours, cv.flip(image, cv.ROTATE_90_CLOCKWISE)

def plot_contours(contours):
    for contour in contours:
        x = np.resize(contour[:, :, 0], len(contour[:, :, 0]))
        y = np.resize(contour[:, :, 1], len(contour[:, :, 0]))
        plt.plot(x, y, c='b')

        # plotting the lines
    plt.show()

def process_contours(contours, min_size=0, line_count=1000):
    result = []
    # has to be more than a certain length
    for contour in contours: 
        if len(contour) >= min_size:
            result.append(contour)
    # only draw top 10 lines 
    result.sort(key= lambda x: len(x), reverse=True)
    return result[:line_count]

def plot_all(original_contours, new_contours, image, print_coordinate): 
    fig, axs = plt.subplots(1, 4)
    axs[0].imshow(image)
    
    axs[1].set_title(f"there are{len(original_contours)} paths")
    for contour in original_contours:
        x = np.resize(contour[:, :, 0], len(contour[:, :, 0]))
        y = np.resize(contour[:, :, 1], len(contour[:, :, 0]))
        axs[1].plot(x, y, c='b')
    
    axs[2].set_title(f"there are{len(new_contours)} paths")
    for contour in new_contours:
        x = np.resize(contour[:, :, 0], len(contour[:, :, 0]))
        y = np.resize(contour[:, :, 1], len(contour[:, :, 0]))
        axs[2].plot(x, y, c='r')

    axs[3].set_title("print coordinate")
    print_x, print_y =  print_coordinate
    axs[3].plot(print_x, print_y, c='g')

    plt.show()

def get_print_coorindates(contours, max_width=12):
    # shrink this down to a 12cm by 12 cm and centered around (5, 3)
    # this is done by finding the maximum x coordinate, and y coordinate 
    # this assumes square
    # draw a line from

    max_x = None
    max_y = None

    all_x = np.array([])
    all_y = np.array([])

    # resize contours
    for contour in contours:
        current_x = np.resize(contour[:, :, 0], len(contour[:, :, 0]))
        x = max(current_x)
        y = max(np.resize(contour[:, :, 1], len(contour[:, :, 0])))
        all_x = np.concatenate([all_x, np.resize(contour[:, :, 0], len(contour[:, :, 0]))], axis=0)
        all_y = np.concatenate([all_y, np.resize(contour[:, :, 1], len(contour[:, :, 0]))], axis=0)

        if max_x is None or x > max_x:
            max_x = x 
        
        if max_y is None or y > max_y:
            max_y = y 
    
    resize_factor = max_x if max_x > max_y else max_y
    resize_factor = 1/resize_factor * max_width
    all_x = (all_x * resize_factor) + 5 
    all_y = (all_y *resize_factor) +3

    return compress_paths(all_x, all_y)

if __name__ == "__main__":
    draw_path_count = 10
    sample_count = 100
    path_to_image = "internet.png"
    #path_to_image = get_image_from_internet("https://t3.gstatic.com/licensed-image?q=tbn:ANd9GcR6XDDIEs3ADIIMe-ZdDG6sLyQ7Pyiu-yBvrWzuvGvpDhNo-GG_91CV0tesc0E7ZLS_")
    
    print(f"Generating path for {path_to_image} with {draw_path_count} paths and sampling {sample_count} for every path")
    original_contours, image = get_contours(path_to_image) 
    new_contours = process_contours(original_contours,line_count=draw_path_count)
    print_x, print_y = get_print_coorindates(new_contours, 10)

    write_to_file("firmware/path.h", print_x, print_y)
    plot_all(original_contours, new_contours, image, (print_x, print_y))