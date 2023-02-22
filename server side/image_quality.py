import cv2
import numpy as np
import os
from PIL import Image, ImageChops



def change_color_to_black_and_white(path):
    original_image = cv2.imread(path, 1)
    # Extracting the height and width of an image
    h, w = original_image.shape[:2]
    # Convert the image to black and white by going over each pixel
    # Each pixel has three features: red, green, blue,
    # and against each color there is a number that indicates a quantity of it.
    # (255 of all colors is white)
    for i in range(h):
        for j in range(w):
            # If the amount of quantities is greater than 160 it is closer to white,
            # else it is a letter = black
            if ((int(original_image[i, j, 0]) + int(original_image[i, j, 1]) + int(
                    original_image[i, j, 2])) / 3) >= 160:
                original_image[i, j] = [255, 255, 255]
            else:
                original_image[i, j] = [0, 0, 0]
    # Save the black and white image
    a=os.path.split(path)[1]
    cv2.imwrite(fr'images/white-black-mezuzas/{a}', original_image)
    return fr'images/white-black-mezuzas/{a}'


def Removes_a_white_frame(path):  # לדרוש שיביאו לי תמונה נקיה בלי לכלוכים מסביב
    im = Image.open(path)
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))  # create a new image white colored
    diff = ImageChops.difference(im, bg)  # computes the 'absolute value of the pixel-by-pixel difference
    # between the two images', which results in a difference image that is returned
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        iii = im.crop(bbox)
        iii.save(path)
    return path

def resolution_and_resize_with_white_background(path_ori, path_dest, r_size=28):
    size = r_size
    img = Image.open(path_ori)
    # resize and keep the aspect ratio
    img.thumbnail((size, size), Image.ANTIALIAS)
    # add the white background
    img_w, img_h = img.size
    background = Image.new('RGB', (size, size), (255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    background.save(path_dest)




def main_image_quality(path):
    path=change_color_to_black_and_white(path)#הופך לשחור לבן
    path=Removes_a_white_frame(path)#הסרת מסגרת לבנה
    return path

def main_change_size(path):
    for l in os.listdir(path):
        for im in os.listdir(fr'{path}/{l}'):
           if im.endswith('.png') or im.endswith('.PNG') or im.endswith('.jpg'):
                resolution_and_resize_with_white_background(fr'{path}/{l}/{im}',
                                                        fr'{path}/{l}/{im}')




