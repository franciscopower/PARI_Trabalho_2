#!/usr/bin/python

import cv2 as cv
import json
from functools import partial
import argparse
from pprint import pprint
import numpy as np

# Global variables
limits_dict = {
    'limits': {
        'BH': {'min': 0, 'max': 255},
        'GS': {'min': 0, 'max': 255},
        'RV': {'min': 0, 'max': 255},
    }
}

def onTrackbar(threshold, channel):
    global limits_dict
    
    if channel == 'minBH':
        limits_dict["limits"]['BH']['min'] = threshold
    elif channel == 'maxBH':
        limits_dict["limits"]['BH']['max'] = threshold
    elif channel == 'minGS':
        limits_dict["limits"]['GS']['min'] = threshold
    elif channel == 'maxGS':
        limits_dict["limits"]['GS']['max'] = threshold
    elif  channel == 'minRV':
        limits_dict["limits"]['RV']['min'] = threshold
    elif  channel == 'maxRV':
        limits_dict["limits"]['RV']['max'] = threshold   
    
    
def main():
    window_name = 'window - Ex3d'
    
    #parsing
    parser = argparse.ArgumentParser(description="Color segmentation")
    parser.add_argument('-hsv', '--segmentate_in_hsv', help = 'If selected, segmentation will be in hsv', action='store_true')
    parser.add_argument('-cn', '--camera_number', help='Number of camera to use', default='0')
    args = parser.parse_args()
    
    hsv_mode = args.segmentate_in_hsv 
    camera_number = int(args.camera_number)

    if hsv_mode:
        track_names = ['min H', 'max H', 'min S', 'max S', 'min V', 'max V']
    else:
        track_names = ['min B', 'max B', 'min G', 'max G', 'min R', 'max R']
    
    
    cap = cv.VideoCapture(camera_number)
    
    cv.namedWindow(window_name)
        #partial function
    trackbarMinBH = partial(onTrackbar, channel='minBH')
    trackbarMaxBH = partial(onTrackbar, channel='maxBH')
    trackbarMinGS = partial(onTrackbar, channel='minGS')
    trackbarMaxGS = partial(onTrackbar, channel='maxGS')
    trackbarMinRV = partial(onTrackbar, channel='minRV')
    trackbarMaxRV = partial(onTrackbar, channel='maxRV')

    cv.createTrackbar(track_names[0], window_name, 0, 255, trackbarMinBH)
    cv.createTrackbar(track_names[1], window_name, 255, 255, trackbarMaxBH)
    cv.createTrackbar(track_names[2], window_name, 0, 255, trackbarMinGS)
    cv.createTrackbar(track_names[3], window_name, 255, 255, trackbarMaxGS)
    cv.createTrackbar(track_names[4], window_name, 0, 255, trackbarMinRV)
    cv.createTrackbar(track_names[5], window_name, 255, 255, trackbarMaxRV)    
    
    k = ''
    while cap.isOpened():
    
        _, I_original = cap.read()
        
        if hsv_mode:
            I = cv.cvtColor(I_original, cv.COLOR_BGR2HSV)
        else:
            I = np.copy(I_original)
        
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
        
        I_segmentated = np.copy(I_original)
        I_segmentated[I_bin == 0] = 0

        cv.imshow(window_name, I_segmentated)    

        k = cv.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord('w') or k == ord('s'):
            # save to json file
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('writing dictionary d to file ' + file_name)
                json.dump(limits_dict, file_handle)  # d is the dicionary
            pass
            
    
    pprint(limits_dict)
    cap.release()
    cv.destroyAllWindows()
    

if __name__ == '__main__':
    main()