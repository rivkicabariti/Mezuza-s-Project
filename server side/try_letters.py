import os
import cv2
import numpy as np
from PIL import Image

def sep_letters(directory, image_line):
    img = cv2.imread(fr'{directory}/{image_line}', 0)
    hight, width = img.shape
    _, blackAndWhite = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    # apply connected component analysis to the blackAndWhite image
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(blackAndWhite, None, None, None, 8, cv2.CV_32S)
    sizes = stats[1:, -1]  # get CC_STAT_AREA component
    img2 = np.zeros((labels.shape), np.uint8)
    dic={}
    print(stats)
    if (nlabels > 2):
        for i in range(1, nlabels):
                    img2[labels == i ] = 255
                    x = stats[i, cv2.CC_STAT_LEFT]  # the starting x coordinate of the component
                    y = stats[i, cv2.CC_STAT_TOP]  # the starting x coordinate of the component
                    w = stats[i, cv2.CC_STAT_WIDTH]  # the width (w) of the component
                    h = stats[i, cv2.CC_STAT_HEIGHT]  # the height (h) of the component
                    area = stats[i, cv2.CC_STAT_AREA]  # The centroid (x, y)-coordinates of the component
                    (cX, cY) = centroids[i]
                    output = img.copy()
                    # clone our original image (so we can draw on it) and then draw
                    # a bounding box surrounding the connected component along with
                    # a circle corresponding to the centroid
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
                    componentMask = (labels == i).astype("uint8") * 255
                    # cv2.imshow("Output", output)
                    # cv2.imshow(f"Connected Component{x,y,w,h}", componentMask)
                    # cv2.waitKey(0)
                    res=cv2.bitwise_not(componentMask)
                    print(res)
                    num_line = os.path.splitext(image_line)[0]
                    dic.update({x:res})
                    # cv2.imwrite(f'images\letters\mezuza1c\line7\{num_line}{nlabels-i}.png', res)

        sortd = sorted(dic.items(), key=lambda x: x[0], reverse=False)
        j=0
        for x, res in sortd:
            cv2.imwrite(fr'images\letters\f\line13\{num_line}a{nlabels - j}.png', res)
            j=j+1
        os.remove(f'{directory}\{image_line}')


def clean_letters(directory, image_line):
    img = cv2.imread(fr'{directory}/{image_line}', 0)
    hight, width = img.shape
    _, blackAndWhite = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    # apply connected component analysis to the blackAndWhite image
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(blackAndWhite, None, None, None, 8, cv2.CV_32S)
    sizes = stats[1:, -1]  # get CC_STAT_AREA component
    img2 = np.zeros((labels.shape), np.uint8)
    dic={}
    f=1
    num_line = os.path.splitext(image_line)[0]
    print(stats)
    if (nlabels > 2):
        for i in range(1, nlabels-1):
                    img2[labels == i ] = 255
                    x_i = stats[i, cv2.CC_STAT_LEFT]  # the starting x coordinate of the component
                    y_i = stats[i, cv2.CC_STAT_TOP]  # the starting x coordinate of the component
                    w_i = stats[i, cv2.CC_STAT_WIDTH]  # the width (w) of the component
                    h_i = stats[i, cv2.CC_STAT_HEIGHT]  # the height (h) of the component
                    (cX, cY) = centroids[i]
                    x = stats[i+1, cv2.CC_STAT_LEFT]  # the starting x coordinate of the component
                    y = stats[i+1, cv2.CC_STAT_TOP]  # the starting x coordinate of the component
                    w= stats[i+1, cv2.CC_STAT_WIDTH]  # the width (w) of the component
                    h = stats[i+1, cv2.CC_STAT_HEIGHT]  # the height (h) of the component
                    x_p = stats[i-1, cv2.CC_STAT_LEFT]  # the starting x coordinate of the component
                    y_p = stats[i-1, cv2.CC_STAT_TOP]  # the starting x coordinate of the component
                    w_p= stats[i-1, cv2.CC_STAT_WIDTH]  # the width (w) of the component
                    h_p = stats[i-1, cv2.CC_STAT_HEIGHT]  # the height (h) of the component

                    output = img.copy()
                    # clone our original image (so we can draw on it) and then draw
                    # a bounding box surrounding the connected component along with
                    # a circle corresponding to the centroid
                    cv2.rectangle(output, (x_i, y_i), (x_i + w_i, y_i + h_i), (0, 255, 0), 3)
                    # cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
                    componentMask = (labels == i).astype("uint8") * 255
                    cv2.imshow("Output", output)
                    cv2.imshow(f"Connected Component", componentMask)
                    cv2.waitKey(0)
                    next=(x >= x_i and (x+w) < (x_i + w_i) and h_i>h)
                    prev= (x_p <= x_i and (x_p+w_p) > (x_i + w_i) and h_i<h_p)
                    if ( next):
                        i=i+2
                        f=0
                        img2[labels == i ] = 255
                        img2[labels==i+1]=255
                        res = cv2.bitwise_not(img2)
                        cv2.imwrite(fr'images\letters\f\line11\{num_line}a.png', res)
                        continue
                    elif prev:
                        i = i + 2
                        f = 0
                        img2[labels == i ] = 255
                        res = cv2.bitwise_not(img2)
                        cv2.imwrite(fr'images\letters\f\line14\{num_line}a.png', res)
                        continue

                    res=cv2.bitwise_not(componentMask)

                    dic.update({x_i:res})
                    # cv2.imwrite(f'images\letters\mezuza1c\line7\{num_line}{nlabels-i}.png', res)

        sortd = sorted(dic.items(), key=lambda x: x[0], reverse=False)
        j=0
        for x, res in sortd:
            cv2.imwrite(fr'images\letters\f\line14\{num_line}a{nlabels - j}.png', res)
            j=j+1
        if f==1:
            os.remove(f'{directory}\{image_line}')




# for l in os.listdir(fr'images/letters/f/line14'):
#     clean_letters(r'images\letters\f\line14',l)

result_file = open('images/results/tttt.txt', 'a', encoding='utf-8')
result_file.write('bh')
result_file.newlines
result_file.writelines('בצד bn')