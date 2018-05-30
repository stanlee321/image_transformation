import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt


# path_to_img = './neg/193.jpg'
path = './data/green'
out_path = './poss/green'

counter = 0
for pic in glob.glob("{}/*.jpg".format(path)):
    try:

        print('pic input', pic)

        img = cv2.imread(pic)
        cols,rows,ch = img.shape
        proportion = 1/3
        # Red Range
        #pts1 = np.float32([[0,0],[rows,0],[0, cols],[rows, cols]])
        #pts2 = np.float32([[0,0],[rows,0],[0, int(proportion*cols)],[rows, int(proportion*cols)]])


        # Yellow Range
        #pts1 = np.float32([[0,0],[rows,0],[0, cols],[rows, cols]])
        #pts2 = np.float32([[0,int(proportion*cols)], [rows,int(proportion*cols)],[0, int(2*proportion*cols)], [rows, int(2*proportion*cols)]])

        # Green Range

        pts1 = np.float32([[0,0],[rows,0],[0, cols],[rows, cols]])
        pts2 = np.float32([[0,int(2*proportion*cols)], [rows,int(2*proportion*cols)],[0, int(3*proportion*cols)], [rows, int(3*proportion*cols)]])



        M = cv2.getPerspectiveTransform(pts1,pts2)
        dst = cv2.warpPerspective(img,M,(rows,cols))
        dst = cv2.resize(dst,(64,192))
        cv2.imwrite('{}/green_{}.jpg'.format(out_path, counter), dst)

        counter +=1
        #plt.subplot(121),plt.imshow(img),plt.title('Input')
        #plt.subplot(122),plt.imshow(dst),plt.title('Output')
        #plt.show()
    except Exception as e:
        print(e, pic)