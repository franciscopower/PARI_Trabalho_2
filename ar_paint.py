#!/usr/bin/python

# PARI ar_paint 2020
# Bruno Neves,
# Diogo Santos, 84861
# Francisco Power,

import cv2 as cv
import json

import numpy as np
import argparse
from time import ctime


def findCentroid(I, limits_dict):
    # binarização
    # encontar o centroide do objeto maior, (x,y)

    return (x, y)

def keyboardMapping(k, I, frame, args, brush_size):
    if k == ord('r'):
        color = (0, 0, 255)
    elif k == ord('g'):
        color = (0, 255, 0)
    elif k == ord('b'):
        color = (255, 0, 0)
    # elif k == ord('e'):
    #     color = (255,255,255) #extra, dá bastante mais trabalho
    elif k == ord('c'):
        if args.augmented_reality:
            I = frame
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
        save_state = cv.imwrite(filename, I)

        if save_state:
            print("Image capture saved") # aplicar colorama stuff
        elif not save_state:
            print("Error: Image capture not saved")


    
    
    else:
        color = (0, 0, 0)
            
    return color, brush_size, I

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
                        action='store_constant',
                        const=False,
                        default='0',
                        help='Definition of paint display')

    args = parser.parse_args()
    print(vars(args))

    # Load json files
    with open(args.json_file) as f:
        Limits_data = json.load(f)

    # Window names
    paint_window = "Paint"
    live_window = "Live feed"

    k = None
    color = (0, 0, 0)
    brush_size = 2

    camera_number = int(args.camera_number)
    cap = cv.VideoCapture(camera_number)
    _, frame = cap.read()
    
    if args.augmented_reality:
        I = np.copy(frame)
    else:
        I = np.ones(frame.shape)*255  
    
    k=''
    while cap.isOpened() and k != ord('q'):
    
        # cv.imshow(window_name, I)
        # myOnMouse = partial(onMouse, I=I, color=color, window_name=window_name, brush_size=brush_size)
        
        # cv.setMouseCallback(window_name, myOnMouse)  
        
        color, brush_size, I = keyboardMapping(k, I, frame, args, brush_size)
        
        k = cv.waitKey(0)
    
    
        

if __name__ == "__main__":
    main()