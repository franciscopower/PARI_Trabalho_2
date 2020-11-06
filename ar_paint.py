#!/usr/bin/python

import cv2 as cv
import numpy as np
import argparse
from time import ctime


def findCentroid(I, limits_dict):
    #convert color mode if needed
    if limits_dict["color_mode"] == 'hsv':
        I = cv.cvtColor(I, cv.COLOR_BGR2HSV)
    
    # segmentate the image
    I_bin = cv.inRange(
        I,
        (
            limits_dict["limits"]['BH']['min'],
            limits_dict["limits"]['GS']['min'],
            limits_dict["limits"]['RV']['min'],
        ),
        (
            limits_dict["limits"]['BH']['max'],
            limits_dict["limits"]['GS']['max'],
            limits_dict["limits"]['RV']['max'],
        )
    )

    #create labels
    _, _, stats, centroids = cv.connectedComponentsWithStats(I_bin, connectivity=4)
    #identify largest area
    stats[np.where(stats[:,4] == stats[:,4].max())[0][0],:] = 0
    big_area_idx = np.where(stats[:,4] == stats[:,4].max())[0][0]
    
    # # discard if area is too small 
    # if stats[big_area_idx,4] < 1000:
    #     x = 0
    #     y = 0
    
    #find centroid
    x,y = centroids[big_area_idx]
    x = int(x)
    y = int(y)

    return (x,y)

def keyboardMapping(k,I,frame,AR,brush_size):
    if k == ord('r'):
        color = (0,0,255)
    elif k == ord('g'):
        color = (0,255,0)
    elif k == ord('b'):
        color = (255,0,0)
    # elif k == ord('e'):
    #     color = (255,255,255) #extra, dá bastante mais trabalho
    elif k == ord('c'):
        if AR:
            I = frame
        else:
            I = np.ones(frame.shape)*255
        color = (0,0,0)
    elif k == 43:
        brush_size += 1
    elif k == 45:
        if brush_size > 1:
            brush_size += -1 
    elif k == ord('w') or k == ord('s'):
        ct = (str(ctime())).replace(' ', '_')
        filename = "drawing_{}.png".format(ct)
        save_state = cv.imwrite(filename, I)

        if save_state:
            print("Image capture saved") # aplicar colorama stuff
        elif not save_state:
            print("Error: Image capture not saved")


    
    
    else:
        color = (0,0,0)
            
    return color, brush_size, I

def main():

    #parser
    parser = argparse.ArgumentParser(description="") #mudar nome
    parser.add_argument('-cn', '--camera_number', help='Number of camera to use', default='0')
    #funcionalidade avançada 2 AR, true of false
    #json file
    args = parser.parse_args()
    
    
    #load json files
    
    #window names
    paint_window = "Paint"
    live_window = "Live feed"
    
        
        
    #inicialização do pincel    
    color = (0,0,0)
    brush_size = 2
    
    
    camera_number = int(args.camera_number)
    cap = cv.VideoCapture(camera_number)
    _,frame = cap.read()
    
    if AR:
        I = np.copy(frame)
    else:
        I = np.ones(frame.shape)*255  
    
    # ------ começa o video -------------------
    k=''
    while cap.isOpened() and k != ord('q'):
    
        # cv.imshow(window_name, I)
        # myOnMouse = partial(onMouse, I=I, color=color, window_name=window_name, brush_size=brush_size)
        
        # cv.setMouseCallback(window_name, myOnMouse)  
        
        color, brush_size, I = keyboardMapping(k,I,frame,AR,brush_size)
        
        k = cv.waitKey(1)
    
    
        
    

if __name__ == "__main__":
    main()