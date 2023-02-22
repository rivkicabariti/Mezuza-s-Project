import os

import cv2
import numpy as np
import pytesseract
from pytesseract import Output

#הנתיב בבית
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
#הנתיב בסמינר
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'




#פונקציות בשביל קיצור פקודות חוזרות
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)

# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated
# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def letters(path):
    import skimage.io as io#תמונה 1
    img = io.imread(str(path))
    custom_config = r'-l heb --psm 6'
    txt = pytesseract.image_to_boxes(img, config=custom_config)
    print(txt)

    # hImg, wImg= img.shape

    boxes = pytesseract.image_to_boxes(img, config=custom_config)
    i=0
    for b in boxes.splitlines():
        b = b.split(' ')
        print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (0, 0), (x + w, y + h),(2,2,2))
        # roi = image[startY:endY, startX:endX]
        image1 = img[0:y+h, 0:x+w]
        cv2.imwrite(fr'images/letters/{i}.png',image1)
        i=i+1
    cv2.imshow('Detected text', img)
    cv2.waitKey(0)

# הצגת התמונות לפי מילים זה עובד טוב
def words(dir,path):
    import skimage.io as io#תמונה 1
    img = io.imread(str(path))
    num_line = os.path.splitext(path)[0]
    os.makedirs(fr'images/letters/{dir}/{num_line}')
    custom_config = r'-l heb --psm 6'
    d = pytesseract.image_to_data(img, output_type=Output.DICT,config=custom_config)
    print(d.keys())
    print(d['text'])
    print(d['conf'])
    i=0
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) >0:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            image1 = img[0:y+h, x:x+w]
            cv2.imwrite(fr'images/letters/{dir}/{num_line}/word{i}.png',image1)
            i=i+1

    cv2.imshow('img', img)

    cv2.waitKey(0)

for l in os.listdir('images/lines/55'):
    words('55',f'images/lines/55/{l}')
#letters('images/letters/7.png')