import cv2 as cv
import numpy as np
from functools import partial

drawing = False
p1 = None

def onMouse(event, x, y, flags, param, I, color, window_name, brush_size):
    global drawing, p1
    
    p2 = None
    
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        p1 = (x,y)
        
    if event == cv.EVENT_MOUSEMOVE and drawing:         
        p2 = (x,y)
        cv.line(I, p1, p2, color, brush_size)
        cv.imshow(window_name, I)
        p1 = (x,y)
        
    if event == cv.EVENT_LBUTTONUP:
        drawing = False
        

def main():
    
    window_name = "Paint"
    I = np.ones((400,600,3))*255
    
    k = None
    color = (0,0,0)
    brush_size = 2
    
    
    while k != ord('q'):
        cv.imshow(window_name, I)
        myOnMouse = partial(onMouse, I=I, color=color, window_name=window_name, brush_size=brush_size)
        
        cv.setMouseCallback(window_name, myOnMouse)  
        k = cv.waitKey(0)
        
        if k == ord('r'):
            color = (0,0,255)
        elif k == ord('g'):
            color = (0,255,0)
        elif k == ord('b'):
            color = (255,0,0)
        elif k == ord('e'):
            color = (255,255,255)
        elif k != ord('s') and k != ord('l'):
            color = (0,0,0)
        
        if k == ord('l'):
            brush_size += 1
        elif k == ord('s'):
            if brush_size > 1:
                brush_size += -1
        


if __name__ == '__main__':
    main()