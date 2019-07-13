import cv2
from random import randint
import numpy as np
import math
import time

# define display window name
windowName = "Joint Bilaterally Filtered Image";

# read in non flashed and flashed images from files and get dimensions
no_flash_img = cv2.imread('./test3a.jpg', cv2.IMREAD_COLOR);
flash_img = cv2.imread('./test3b.jpg', cv2.IMREAD_COLOR);
width = np.size(no_flash_img, 1)
height = np.size(no_flash_img, 0)

def get_neighbours(d, x, y, k):

    # loop through each neighbour in the mask
    for i in range(-1 * middle, middle + 1):
        for j in range(-1 * middle, middle + 1):
            if i == 0 and j == 0:
                continue
            elif x + i < 0 or y + j < 0 or x + i >= height or y + j >= width:
                # if out of bounds then equate the out of bounds neighbours' intensities to the centre pixel's intensity
                no_flash_intensities[middle + i][middle + j] = no_flash_img[x][y][k]
                flash_intensities[middle + i][middle + j] = flash_img[x][y][k]
            else:
                # otherwise fill in correct values of the flash and no flash intensity matrices
                no_flash_intensities[middle + i][middle + j] = no_flash_img[x + i][y + j][k]
                flash_intensities[middle + i][middle + j] = flash_img[x + i][y + j][k]
            distances[middle + i][middle + j] = math.sqrt(i**2 + j**2)
    return (no_flash_intensities, flash_intensities, distances)

def gaussian_function(x, sigma):

    # calculate the gaussian of the distance or the intensity difference
    return 1/((sigma*math.pi)**(1/2)) * math.exp(-((x**2)/(2*(sigma**2))))
       
def joint_bilateral_filter(d, sigma_colour, sigma_space):

    start = time.time()

    # loop through each pixel and perform the joint bilateral filter on each colour channel
    for x in range(0, width):
        for y in range(0, height):
            for k in range(0, 3):
                no_flash_intensity = no_flash_img[y][x][k]
                flash_intensity = flash_img[y][x][k]
                
                # get the neighbourhood intensities
                neighbour_info = get_neighbours(d, y, x, k)
                no_flash_intensities = neighbour_info[0]
                flash_intensities = neighbour_info[1]
                distances = neighbour_info[2]

                # use formula on each pixel in neighbourhood
                total = 0
                normalisation = 0
                for i in range(0, d):
                    for j in range(0, d):
                        if i == middle and j == middle:
                            continue
                        # calculate differences and get their gaussian values
                        distance = distances[i][j]
                        intensity_difference = flash_intensity - flash_intensities[i][j]
                        no_flash_intensity = no_flash_intensities[i][j]
                        g1 = gaussian_function(distance, sigma_space)
                        g2 = gaussian_function(intensity_difference, sigma_colour)
                        # multiply and then add them up as per formula
                        total += g1*g2*no_flash_intensity
                        normalisation += g1*g2
                no_flash_img[y][x][k] = total/normalisation    # normalisation 

    # recording time taken and returning value
    end = time.time()
    time_taken = end - start
    minutes = int(time_taken/60)    
    seconds = round(time_taken - minutes*60, 2)
    print("Total time taken: " + str(minutes) + ":" + str(seconds))
    return no_flash_img

# check it has loaded
if not no_flash_img is None and not flash_img is None:

    # setting the parameter values
    d, sigma_colour, sigma_space = 7, 5, 5

    # creating the intensity and distance matrices
    flash_intensity_differences = np.zeros(shape = (d, d), dtype = int)
    no_flash_intensities = np.zeros(shape = (d, d), dtype = int)
    flash_intensities = np.zeros(shape = (d, d), dtype = int)
    distances = np.zeros(shape = (d, d), dtype = float)
    middle = math.floor(d/2)    # calculating the center index of neighbourhood

    # calling joint bilateral filter on the images using assiged parameters and displaying result in window
    new_img = joint_bilateral_filter(d, sigma_colour, sigma_space)
    cv2.imshow(windowName, new_img);
    key = cv2.waitKey(0);
    
    if (key == ord('x')):
        cv2.destroyAllWindows();
else:
    print("Image file failed to load.");
    
