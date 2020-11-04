#!/usr/bin/python

import cv2
from functools import partial
import argparse
from pprint import pprint

# Global variables
limits_dict = {
    'limits': {
        'BH': {'min': 0, 'max': 255},
        'GS': {'min': 0, 'max': 255},
        'RV': {'min': 0, 'max': 255},
    }
}

def onTrackbar(threshold, I, window_name, channel):
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
    
    I_bin = cv2.inRange(
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

    cv2.imshow(window_name, I_bin)
    
    
def main():
    window_name = 'window - Ex3d'
    
    #parsing
    parser = argparse.ArgumentParser(description="Color segmentation")
    parser.add_argument('-hsv', '--segmentate_in_hsv', help = 'If selected, segmentation will be in hsv', action='store_true')
    args = parser.parse_args()
    
    hsv_mode = args.segmentate_in_hsv    
    
    #Load Image
    image_filename = "../img/atlas2000_e_atlasmv.png"
    I = cv2.imread(image_filename, cv2.IMREAD_COLOR)
    
    track_names = ['min B', 'max B', 'min G', 'max G', 'min R', 'max R']
    
    if hsv_mode:
        I = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)
        track_names = ['min H', 'max H', 'min S', 'max S', 'min V', 'max V']
    
    
    #Create window
    cv2.namedWindow(window_name)
        
    #partial function
    trackbarMinBH = partial(onTrackbar, I=I, window_name=window_name, channel='minBH')
    trackbarMaxBH = partial(onTrackbar, I=I, window_name=window_name, channel='maxBH')
    trackbarMinGS = partial(onTrackbar, I=I, window_name=window_name, channel='minGS')
    trackbarMaxGS = partial(onTrackbar, I=I, window_name=window_name, channel='maxGS')
    trackbarMinRV = partial(onTrackbar, I=I, window_name=window_name, channel='minRV')
    trackbarMaxRV = partial(onTrackbar, I=I, window_name=window_name, channel='maxRV')
    
    cv2.createTrackbar(track_names[0], window_name, 0, 255, trackbarMinBH)
    cv2.createTrackbar(track_names[1], window_name, 255, 255, trackbarMaxBH)
    cv2.createTrackbar(track_names[2], window_name, 0, 255, trackbarMinGS)
    cv2.createTrackbar(track_names[3], window_name, 255, 255, trackbarMaxGS)
    cv2.createTrackbar(track_names[4], window_name, 0, 255, trackbarMinRV)
    cv2.createTrackbar(track_names[5], window_name, 255, 255, trackbarMaxRV)
    
    trackbarMinBH(0)

    cv2.waitKey(0)
    
    pprint(limits_dict)
    
    
    

if __name__ == '__main__':
    main()