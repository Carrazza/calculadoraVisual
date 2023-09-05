import cv2
import numpy as np
from bresenham import bresenham

def get(image):
    image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)


    max_y_coords = None
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] < 10: 
                max_y_coords = (x, y)
                break
        if max_y_coords is not None:
            break


    max_x_coords = None
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            if image[y, x] < 10: 
                max_x_coords = (x, y)
                break
        if max_x_coords is not None:
            break


    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    color_image[max_y_coords[1], max_y_coords[0]] = (0, 0, 255) 
    color_image[max_x_coords[1], max_x_coords[0]] = (0, 255, 0)  


    black_white=[0,0]
    line_coords = list(bresenham(max_x_coords[0], max_x_coords[1], max_y_coords[0], max_y_coords[1]))
    for coord in line_coords:
        if image[coord[1],coord[0]] < 180: black_white[0] += 1
        else: black_white[1] += 1

        color_image[coord[1], coord[0]] = (0, 0, 255)  # Red pixel

    # Save the modified color image with the line pixels
    #cv2.imwrite('imagemDahora.png', color_image)
    dist=abs(max_x_coords[1]-max_y_coords[1])


    if(black_white[1]/black_white[0] > 0.9): 
        
        
        if(dist < 10):
            #print("sub")
            return "-"
            
        else:
            #print("soma")
            return "+"

        

            
            
    else: return "-"