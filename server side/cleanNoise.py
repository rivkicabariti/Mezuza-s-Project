import cv2
import numpy as np
from PIL import Image
import os


# נעזרתי בhttps://www.pyimagesearch.com/2021/02/22/opencv-connected-component-labeling-and-analysis/
def clean_noises(directory, image_line):
    img = cv2.imread(fr'{directory}/{image_line}', 0)
    hight, width = img.shape
    _, blackAndWhite = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    # apply connected component analysis to the blackAndWhite image
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(blackAndWhite, None, None, None, 8, cv2.CV_32S)
    sizes = stats[1:, -1]  # get CC_STAT_AREA component
    img2 = np.zeros((labels.shape), np.uint8)

    for i in range(0, nlabels - 1):
        # extract the connected component statistics and centroid for
        # the current label
        x = stats[i, cv2.CC_STAT_LEFT]  # the starting x coordinate of the component
        y = stats[i, cv2.CC_STAT_TOP]  # the starting x coordinate of the component
        w = stats[i, cv2.CC_STAT_WIDTH]  # the width (w) of the component
        h = stats[i, cv2.CC_STAT_HEIGHT]  # the height (h) of the component
        area = stats[i, cv2.CC_STAT_AREA]  # The centroid (x, y)-coordinates of the component
        (cX, cY) = centroids[i]

        small_dotted = sizes[i] >= 20
        down = y < hight / 2 + 7
        up = y > 0 and (y + h) < (hight / 2)

        if (small_dotted and down):
                img2[labels == i + 1] = 255
                # output = img.copy()

                # clone our original image (so we can draw on it) and then draw
                # a bounding box surrounding the connected component along with
                # a circle corresponding to the centroid
                # cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
                # componentMask = (labels == i).astype("uint8") * 255
                # cv2.imshow("Output", output)
                # cv2.imshow("Connected Component", componentMask)
                # cv2.waitKey(0)
    # change again to white-background and black-letters
    res = cv2.bitwise_not(img2)
    cv2.imwrite(fr'{directory}/{image_line}', res)


def clean_noises2(directory, image_line):  # כדי למחוק את החלק העליון דרוש תיקון דחוףףף
    img = cv2.imread(fr'{directory}/{image_line}', 0)
    hight, width = img.shape
    _, blackAndWhite = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(blackAndWhite, None, None, None, 8, cv2.CV_32S)
    sizes = stats[1:, -1]  # get CC_STAT_AREA component
    img2 = np.zeros(labels.shape, np.uint8)

    for i in range(0, nlabels - 1):
        # if sizes[i] >= 40:   #filter small dotted regions
        #     img2[labels == i + 1] = 255
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]

        if (y + h) > 1:  # (cY)>=(hight / 2)or y!=0 or area>=hight/3
            print(f'x {x} y {y} w {w} h {h} area {area} cx {cX} cy{cY}')
            img2[labels == i + 1] = 255

    res = cv2.bitwise_not(img2)
    cv2.imwrite(fr'{directory}/{image_line}', res)




def main_cleaner(path):
    for line in os.listdir(path):
        if line.endswith('.jpg') or line.endswith('.png') or line.endswith('.PNG'):
            clean_noises(path, line)

