#!/usr/bin/python

# PARI ar_paint 2020
# Bruno Nunes, 80614
# Diogo Santos, 84861
# Francisco Power, 84706

# IMPORTS -------------------------
import cv2 as cv
import json
from colorama import Fore, Style
import numpy as np
import argparse
from time import ctime
# ---------------------------------

def findCentroid(frame, limits_dict, SP):
    """Find the centroid of the largest blob given in an image, given a certain dictionary with binarization limits
        If shake prevention (SP) mode is active, return centroid as (0,0) 
        
    Args:
        frame (np.ndarray): Original Image
        limits_dict (dictionary): dictionary with binarization limits and color space
        SP (boolean): Shake prevention mode

    Returns:
        tuple: (x,y) coordinates of centroid of largest blob
    """
    
    #create copy of frame
    frame_one_area = np.copy(frame)
    
    #convert color mode if needed
    if limits_dict["color_mode"] == 'hsv':
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # segmentate the image
    I_bin = cv.inRange(
        frame,
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
    _, labels, stats, centroids = cv.connectedComponentsWithStats(I_bin, connectivity=4)

    #identify largest area
    stats[np.where(stats[:, 4] == stats[:, 4].max())[0][0], :] = 0
    big_area_idx = np.where(stats[:, 4] == stats[:, 4].max())[0][0]

    #find centroid
    x, y = centroids[big_area_idx]
    x = int(x)
    y = int(y)

    if len(stats) != 1:
        #show selected area
        M_SA = np.zeros(labels.shape, dtype=np.uint8)
        M_SA[labels == big_area_idx] = 255
        frame_one_area[M_SA == 255] = (0,255,0)

        #show centroid of selected area
        frame_one_area = cv.circle(frame_one_area, (x,y), 5, (0,0,255), -1)

    #show binarized image
    cv.imshow('bin img', I_bin)

    #use shake prevention
    if SP:
        # discard if area is too small
        if stats[big_area_idx, 4] < frame.shape[0]*frame.shape[1]*0.01:
            x = 0
            y = 0
        # discard if it cannot find any whitepoints
        if len(stats) == 1:
            x = 0
            y = 0
    else:
        pass
    
    return (x,y), frame_one_area

# -------------------------------------------------------------------------

def keyboardMapping(k, I, I_f, frame, AR, brush_size, opacity, clr):
    """[summary]

    Args:
        k ([type]): [description]
        I ([type]): [description]
        I_f ([type]): [description]
        frame ([type]): [description]
        AR ([type]): [description]
        brush_size ([type]): [description]
        opacity ([type]): [description]
        clr ([type]): [description]

    Returns:
        [type]: [description]
    """
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
            print(Fore.GREEN + "\nImage capture saved as\n" + Fore.RESET + filename) # apply colorama stuff
        else:
            print(Fore.RED + "Error: Image capture not saved" + Fore.RESET)
    elif k == ord('p') or k == ord('k'):
        if AR:
            color = (255,255,255)
        else:
            color = (0, 0, 0)
    elif k == ord('h') and opacity < 1.0:
        opacity = opacity + 0.1
    elif k == ord('l') and opacity >0.05:
        opacity = opacity - 0.1
            
    return color, brush_size, opacity, I

# -------------------------------------------------------------------------

def paint(drawing, frame, I, p1, p2, color, brush_size, AR, opacity):    
    """[summary]

    Args:
        drawing ([type]): [description]
        frame ([type]): [description]
        I ([type]): [description]
        p1 ([type]): [description]
        p2 ([type]): [description]
        color ([type]): [description]
        brush_size ([type]): [description]
        AR ([type]): [description]
        opacity ([type]): [description]

    Returns:
        [type]: [description]
    """

    if drawing:
        cv.line(I, p1, p2, color, brush_size)
        
    I_f = np.copy(I)
    
    if AR:
        if opacity == 1:
            I_f = np.copy(frame)
            hsv = np.copy(I)
            hsv = hsv.astype(np.uint8)
            hsv = cv.cvtColor(hsv, cv.COLOR_BGR2HSV)
            M = 255-cv.inRange(hsv, (0, 0, 0), (255, 0, 0))
            M = M.astype(np.uint8)
            I_f[M == 255] = I[M == 255]
            
        else:
            I_f = I_f.astype(np.uint8)
            I_f = cv.addWeighted(frame, 1, I_f, opacity, 0)
    
    return I, I_f

# -------------------------------------------------------------------------

def main():
    """[summary]
    """
    # ----------DEFINITION OF PARSER ARGUMENTS----------------
    parser = argparse.ArgumentParser(description=Fore.RED + 'Augmented Reality Paint - ' + Style.RESET_ALL + 'Paint the world around you')
    parser.add_argument('-jf',
                        '--json_file',
                        type=str,
                        default=None,
                        required=True,
                        help='json file with this ' + Fore.GREEN + 'limits ' + Style.RESET_ALL + 'defined in color segmenter')
    parser.add_argument('-cn',
                        '--camera_number',
                        type=int,
                        help='Number of ' + Fore.GREEN + ' camera ' + Style.RESET_ALL + 'to use',
                        default='0')
    parser.add_argument('-AR',
                        '--augmented_reality',
                        action='store_true',
                        help='Definition of ' + Fore.GREEN + 'paint type ' + Style.RESET_ALL + 'display')
    parser.add_argument('-USP',
                        '--use_shake_prevention',
                        action='store_true',
                        help='Add function - ' + Fore.GREEN + 'shake prevention' + Style.RESET_ALL)


    args = parser.parse_args()
    
    AR = args.augmented_reality
    SP = args.use_shake_prevention

    # Load json files
    with open(args.json_file) as f:
        limits_dict = json.load(f)

#print program initialization
    keyboard_shortcuts = Fore.RED + "Keyboard shortcuts\n" + Fore.RESET
    keyboard_shortcuts += """\n
    r : change brush color to RED \n
    g : change brush color to GREEN \n 
    b : change brush color to BLUE \n 
    p, k : change brush color to BLACK \n 
    + : increase brush size \n 
    - : decrease brush size \n 
    h : increase brush opacity \n 
    l : decrease brush opacity \n 
    e : eraser brush \n 
    c : clear all drawings \n 
    w, s : write/save drawing to file\n"""

    hello_text = "----------------------------------------------------------\n\n"
    hello_text += Fore.GREEN + "AUGMENTED REALITY PAINT\n" + Fore.RESET
    hello_text += "Use a colored object to paint the world around you\n\n"
    hello_text += keyboard_shortcuts

    print(hello_text)
    
    print(Fore.RED + "Your settings: " + Fore.RESET)
    print(vars(args))

    camera_number = int(args.camera_number)
    cap = cv.VideoCapture(camera_number)
    _,frame = cap.read()
    
    # initialize base canvas and brush color
    if AR:
        I = np.zeros(frame.shape)
        color = (255, 255, 255)
    else:
        I = np.ones(frame.shape)*255   
        color = (0,0,0)

    # initialize final canvas
    I_f = np.copy(I)   
    
    #brush initializarion    
    brush_size = 10
    opacity = 1.0
    
    k =''
    p1 = (0,0)
    drawing = False
    # ------ video starts-------------------
    while cap.isOpened() and k != ord('q'):
    
        _,frame = cap.read()
        p2, frame = findCentroid(frame, limits_dict, SP)
        
        if p1 == (0, 0) or p2 ==(0, 0):
            drawing = False
        else: 
            drawing = True
        
        I, I_f = paint(drawing, frame, I, p1, p2, color, brush_size, AR, opacity)
        
        color, brush_size, opacity, I = keyboardMapping(k, I, I_f, frame, AR, brush_size, opacity, color)
        p1 = p2
        
        cv.imshow("Live feed", frame)
        cv.imshow("Paint", I_f)

        k = cv.waitKey(1)
        
    cv.destroyAllWindows()

    print("\nThank you for using AR Paint\nCreated by:\n\t- Bruno Nunes\n\t- Diogo Santos\n\t- Francisco Power\n")    
    print("----------------------------------------------------------\n\n")

        

if __name__ == "__main__":
    main()