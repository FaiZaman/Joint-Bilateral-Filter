import cv2
from random import randint
import numpy as np
import math
import time

# define display window name
original_window_name = "Original Image";
new_window_name = "Bilaterally Filtered Image"

# read an image from the specified file (in colour)
img = cv2.imread('./test1.png', cv2.IMREAD_COLOR);

# img, int d, sigmaColour, sigmaSpace
# d = neighbourhood size
# sigmaColour = spatial proximity's effect increased (smaller distance means greater effect)
# sigmaSpace = intensity difference's effect increased (smaller difference means greater effect)

# check it has loaded
if not img is None:

    new_img = cv2.bilateralFilter(img, 5, 10000, 10000);
    
    #cv2.imshow(original_window_name, img);
    #key = cv2.waitKey(0); # wait
    
    cv2.imshow(new_window_name, new_img);
    key = cv2.waitKey(0); # wait
    
    if (key == ord('x')):
        cv2.destroyAllWindows();
else:
    print("No image file successfully loaded.");
    
