import cv2
import numpy as np
import glob

# path_to_img = './neg/193.jpg'
path = './data/green'
out_path = './process/'
gamma = [1.0, 5.0, 10.0]
scale = 8


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def segment_by_color():
    counter = 0
    for g in gamma:
        for pic in glob.glob("{}/*.jpg".format(path)):
            try:
                print('pic input', pic)
                img = cv2.imread(pic)

                img_gamma = adjust_gamma(img, gamma=g)

                new_shape = (int(8 * scale), int(24 * scale))

                img_crop = cv2.resize(img_gamma, new_shape, interpolation=cv2.INTER_CUBIC)

                hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)

                lower_red = np.array([104, 21, 114])
                upper_red = np.array([180, 255, 255])

                lower_yellow = np.array([5, 45, 209])
                upper_yellow = np.array([40, 255, 255])

                lower_green = np.array([40, 20, 0])
                upper_green = np.array([90, 255, 255])

                mask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
                mask2 = cv2.inRange(hsv, lower_red, upper_red)
                mask3 = cv2.inRange(hsv, lower_green, upper_green)

                mask = mask1 + mask2 + mask3

                res = cv2.bitwise_and(img_crop, img_crop, mask=mask)
                blur = cv2.GaussianBlur(res, (15, 15), 0)
                _, puck = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY)

                if np.mean(puck) < 2:
                    print('pic',pic)
                    print(np.mean(puck))
                    cv2.imwrite('./{}/else/else_{}.jpg'.format(out_path, counter), puck)
                else:
                    print('input', pic)
                    cv2.imwrite('./{}/green/green_{}.jpg'.format(out_path, counter), puck)

                counter += 1

            except Exception as e:
                print('This dude {} as {}'.format(pic, e))
        print('gamam', g)

if __name__ == '__main__':
    segment_by_color()
