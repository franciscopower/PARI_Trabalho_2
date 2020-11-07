import cv2 as cv
import numpy as np

# frame = cv.imread('atlascar2.png', 1)*0

# I_bin = cv.inRange(frame,(106,33,0),(126,172,102))

# _, _, stats, centroids = cv.connectedComponentsWithStats(I_bin, connectivity=4)

# stats[np.where(stats[:,4] == stats[:,4].max())[0][0],:] = 0
# big_area_idx = np.where(stats[:,4] == stats[:,4].max())[0][0]
# x,y = centroids[big_area_idx]
# x = int(x)
# y = int(y)

# print(big_area_idx)
# print(stats)
# print(len(stats))
# print(x,y)
# I_bin_color = frame*0
# I_bin_color[:,:,0] = I_bin
# I_bin_color[:,:,1] = I_bin
# I_bin_color[:,:,2] = I_bin
# I_bin_color = cv.circle(I_bin_color, (x,y), 5, (0,0,255), -1)

# cv.imshow('w', I_bin_color)

#-------------------------------------------------------------



frame = cv.imread('drawing_Sat_Nov__7_12:03:15_2020.png', 1)

I = cv.imread('drawing_Sat_Nov__7_12:04:12_2020.png')
hsv = cv.cvtColor(I, cv.COLOR_BGR2HSV)

M = 255-cv.inRange(hsv, (0,0,254), (255,1,255))
M = M.astype(np.uint8)


final = np.copy(frame)
final[M == 255] = I[M==255]










cv.imshow('w',M)
cv.imshow('I', I)
cv.imshow('final', final)

cv.waitKey(0)


