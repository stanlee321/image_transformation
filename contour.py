import numpy as np 
import cv2 
import matplotlib.pyplot as plt



def get_centroid(x, y, w, h):
	x1 = int(w / 2)
	y1 = int(h / 2)

	cx = x + x1
	cy = y + y1

	return (cx, cy)


# Adjust the minimum size of the blog matching contour
min_contour_width 	= 5
min_contour_height  = 5

img = cv2.imread('g.jpg')
k 		= 15
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
smooth_frame = cv2.GaussianBlur(imgray, (k, k), 1.5)
ret, thresh = cv2.threshold(smooth_frame, 127, 255, 0)
img_bin = cv2.morphologyEx(thresh, cv2.MORPH_ELLIPSE, np.ones((3, 3), dtype=int))

img2, contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for (i, contour) in enumerate(contours):
	(x, y, w, h) = cv2.boundingRect(contour)
	contour_valid = (w >= min_contour_width) and (h >= min_contour_height)
	if not contour_valid:
		continue
	centroid = get_centroid(x, y, w, h)


cv2.circle(img2, centroid,2,(0,255,255),-1)
print('contours', contours)
cv2.imshow('thress', img2)
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(img_bin),plt.title('Output')
plt.show()