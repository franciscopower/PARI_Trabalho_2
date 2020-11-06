#!/usr/bin/python

import cv2 as cv
import numpy as np
import argparse

def findCentroid(I, limits_dict):
    #binarização
    #encontar o centroide do objeto maior, (x,y)

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
        pass #guradar imagem
    
    
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
    
        
    k = None
    color = (0,0,0)
    brush_size = 2
    
    
    camera_number = int(args.camera_number)
    cap = cv.VideoCapture(camera_number)
    _,frame = cap.read()
    
    if AR:
        I = np.copy(frame)
    else:
        I = np.ones(frame.shape)*255  
    
    k=''
    while cap.isOpened() and k != ord('q'):
    
        # cv.imshow(window_name, I)
        # myOnMouse = partial(onMouse, I=I, color=color, window_name=window_name, brush_size=brush_size)
        
        # cv.setMouseCallback(window_name, myOnMouse)  
        
        color, brush_size, I = keyboardMapping(k,I,frame,AR,brush_size)
        
        k = cv.waitKey(0)
    
    
        
    

if __name__ == "__main__":
    main()