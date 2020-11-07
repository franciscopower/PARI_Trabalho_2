#!/usr/bin/python

# PARI ar_paint 2020
# Bruno Nunes, 80614
# Diogo Santos, 84861
# Francisco Power, 84706

import cv2 as cv
import json

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
    #find centroid
    x,y = centroids[big_area_idx]
    x = int(x)
    y = int(y)
    
    # discard if area is too small 
    if stats[big_area_idx,4] < I.shape[0]*I.shape[1]*0.01:
        x = 0
        y = 0
    
    # discard if it cannot find any whitepoints
    if len(stats) == 1:
        x=0
        y=0
        
    #show binarized image
    cv.imshow('bin img',I_bin)
    
    return (x,y)

def keyboardMapping(k, I, I_f, frame, AR, brush_size, opacity, clr):
    color = clr
    
    if k == ord('r'):
        color = (0, 0, 255)
    elif k == ord('g'):
        color = (0, 255, 0)
    elif k == ord('b'):
        color = (255, 0, 0)
    elif k == ord('e'):
        if AR:
            color = (0,0,0)
        else:
            color = (255,255,255)
    elif k == ord('c'):
        if AR:
            I = np.ones(frame.shape)*0
            color = (255,255,255)
        else:
            I = np.ones(frame.shape)*255
            color = (0, 0, 0)
    elif k == 43:
        brush_size += 1
    elif k == 45:
        if brush_size > 1:
            brush_size += -1 
    elif k == ord('w') or k == ord('s'): 
        ct = (str(ctime())).replace(' ', '_')
        filename = "drawing_{}.png".format(ct)
        save_state = cv.imwrite(filename, I_f)
        #add delay ?
        if save_state:
            print("Image capture saved") # apply colorama stuff
        else:
            print("Error: Image capture not saved")
    elif k == ord('p') or k == ord('k'):
        if AR:
            color = (255,255,255)
        else:
            color = (0, 0, 0)
    elif k == ord('h') and opacity <1:
        opacity += 0.1
    elif k == ord('l') and opacity >0:
        opacity -= 0.1
            
    return color, brush_size, opacity, I

def paint(drawing, frame, I, p1, p2, color, brush_size, AR, opacity):    
    
    if drawing:
        cv.line(I, p1, p2, color, brush_size)
        
    I_f = np.copy(I)
    
    if AR:
        if opacity == 1:
            I_f = np.copy(frame)
            hsv = np.copy(I)
            hsv = hsv.astype(np.uint8)
            hsv = cv.cvtColor(hsv, cv.COLOR_BGR2HSV)
            M = 255-cv.inRange(hsv, (0,0,0), (255,0,0))
            M = M.astype(np.uint8)
            I_f[M==255] = I[M==255]
            
        else:
            I_f = I_f.astype(np.uint8)
            I_f = cv.addWeighted(frame, 1, I_f, opacity, 0)
    
    return I,I_f


def main():
    # ----------DEFINITION OF PARSER ARGUMENTS----------------
    parser = argparse.ArgumentParser(description='Definition of test mode')
    parser.add_argument('-jf',
                        '--json_file',
                        type=str,
                        default=None,
                        required=True,
                        help='json file with this limits defined in color segmenter')
    parser.add_argument('-cn',
                        '--camera_number',
                        type=int,
                        help='Number of camera to use',
                        default='0')
    parser.add_argument('-AR',
                        '--augmented_reality',
                        action='store_true',
                        help='Definition of paint display')

    args = parser.parse_args()
    print(vars(args))
    
    AR = args.augmented_reality

    # Load json files
    with open(args.json_file) as f:
        limits_dict = json.load(f)

    # Window names
    paint_window = "Paint"
    live_window = "Live feed" 

    camera_number = int(args.camera_number)
    cap = cv.VideoCapture(camera_number)
    _,frame = cap.read()
    
    # initialize base canvas and brush color
    if AR:
        I = np.zeros(frame.shape)
        color = (255,255,255)
    else:
        I = np.ones(frame.shape)*255   
        color = (0,0,0)  
        
    # initialize final canvas
    I_f = np.copy(I)   
    
    #brush initializarion    
    brush_size = 2
    opacity = 0.5
    
    k=''
    p1 = (0,0)
    drawing = False
    # ------ video starts-------------------
    while cap.isOpened() and k != ord('q'):
    
        _,frame = cap.read()
        p2 = findCentroid(frame, limits_dict)
        if p1 == (0,0) or p2 ==(0,0):
            drawing = False
        else: 
            drawing = True
        
        I, I_f = paint(drawing, frame, I, p1, p2, color, brush_size, AR, opacity)
        
        color, brush_size, opacity, I = keyboardMapping(k, I, I_f, frame, AR, brush_size, opacity, color)
        p1 = p2
        
        cv.imshow(live_window, frame)
        cv.imshow(paint_window, I_f)

        k = cv.waitKey(1)
        
cv.destroyAllWindows()
    
        

if __name__ == "__main__":
    main()