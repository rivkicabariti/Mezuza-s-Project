#צריך להתקין:
# opencv-contrib-python
# pytesseract
# tesseract




import cv2
import numpy as np
import pytesseract
from pytesseract import Output

#הנתיב בבית
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
#הנתיב בסמינר
#pytesseract.pytesseract.tesseract_cmd =''




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




#הצגת זיהוי הטקסט בתמונה -רגילה אות אות
# img = cv2.imread('images/t_id.png')
#
# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
#
# cv2.imshow('img', img)
# cv2.waitKey(0)


#הצגת התמונות לפי מילים

#תמונה 1
img = cv2.imread('images/t_id.png')
d = pytesseract.image_to_data(img, output_type=Output.DICT)
print(d.keys())
print(d['text'])
print(d['conf'])

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


#תמונה 2
img1 = cv2.imread('images/t_2.png')
d1 = pytesseract.image_to_data(img1, output_type=Output.DICT)
print(d1.keys())
print(d1['text'])
print(d1['conf'])

n_boxes1 = len(d1['text'])
for i in range(n_boxes1):
    if int(d1['conf'][i]) > 60:
        (x, y, w, h) = (d1['left'][i], d1['top'][i], d1['width'][i], d1['height'][i])
        img1 = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)

#מציאת תז ב2 תמונות שונות
a = '0'
b = '1'
for i in range(n_boxes):
    if d['text'][i] == 'Id:':
        a = d['text'][i+1]
        i = n_boxes
for i in range(n_boxes1):
    if d1['text'][i] == 'Id:':
        b = d1['text'][i+1]
        i = n_boxes1
if a == b:
    print(a)

cv2.imshow('img', img)
cv2.imshow('img1', img1)

cv2.waitKey(0)



#חיפוש התאריך בתמונה
# import re
#
# d = pytesseract.image_to_data(img, output_type=Output.DICT)
# keys = list(d.keys())
#
# date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
#
# n_boxes = len(d['text'])
# for i in range(n_boxes):
#     if int(d['conf'][i]) > 60:
#         if re.match(date_pattern, d['text'][i]):
#             (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#             img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# #רק ספרות
# # custom_config = r'--oem 3 --psm 6 outputbase digits'
# # print(pytesseract.image_to_string(img, config=custom_config))
#
# cv2.imshow('img', img)
# cv2.waitKey(0)
