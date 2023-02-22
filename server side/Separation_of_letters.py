import cv2
import numpy as np
from PIL import Image
import os


def num_of_black_pixels(image_path):
    image = Image.open(str(image_path))
    arr = np.array(image)
    countb = 0
    countw = 0
    for i in range(image.height):
        for j in range(image.width):
            if (arr[i][j].all() == 0):
                countb += 1
            else:
                countw += 1
    return countb, countw


def cut_lines(path_to_mezuza):
    blacks, whites = num_of_black_pixels(path_to_mezuza)
    image = Image.open(path_to_mezuza)
    arr = np.array(image)
    rows_suspected_list = []  # A list in which the rows that are suspected as spaces are inserted
    for i in range(image.height):
        counter = 0  # Counts the number of black pixels in a row
        for j in range(image.width):
            if arr[i][j].all() == 0:  # If the pixel is black
                counter += 1
        if counter >= (0.001 * blacks):  # עובד מעולה
            rows_suspected_list.append(i)
    lines_list = [rows_suspected_list[1]]  # List of pixel rows of beginning and end of a line in a mezuzah
    for i in range(1, len(rows_suspected_list)):
        if (rows_suspected_list[i] - rows_suspected_list[i - 1]) > 3:
            lines_list.append(rows_suspected_list[i])
    dire = os.path.split(path_to_mezuza)[1]
    dire = os.path.splitext(dire)[0]
    os.mkdir(fr'images/lines/{dire}')
    for i in range(len(lines_list) - 1):
        # Crop the line from the image
        image1 = image.crop((0, lines_list[i] - int(image.height * 0.02), image.width, lines_list[i + 1]))
        image1.save(fr'images/lines/{dire}/line{i + 1}.png')
    # Save the last row
    image1 = image.crop((0, lines_list[len(lines_list) - 1] - int(image.height * 0.02), image.width, image.height))
    image1.save(fr'images/lines/{dire}/line{len(lines_list)}.png')
    return fr'images/lines/{dire}'


def cut_line_21(dir, line_21):
    blacks, whites = num_of_black_pixels(fr'images/lines/{dir}/{line_21}')
    image = Image.open(fr'images/lines/{dir}/{line_21}')
    arr = np.array(image)
    rows_suspected_list = []  # A list in which the rows that are suspected as spaces are inserted
    for i in range(image.height):
        counter = 0  # Counts the number of black pixels in a row
        for j in range(image.width):
            if arr[i][j].all() == 0:  # If the pixel is black
                counter += 1
        if counter >= (0.01 * blacks):
            rows_suspected_list.append(i)
    lines_list = [rows_suspected_list[0]]  # List of pixel rows of beginning and end of a line in a mezuzah
    for i in range(1, len(rows_suspected_list)):
        if (rows_suspected_list[i] - rows_suspected_list[i - 1]) > 3:
            lines_list.append(rows_suspected_list[i])
    for i in range(len(lines_list) - 1):
        # Crop the line from the image
        image1 = image.crop((0, lines_list[i] - int(image.height * 0.13), image.width, lines_list[i + 1]))
        image1.save(fr'images/lines/{dir}/line21.png')
    # Save the last row
    image1 = image.crop((0, lines_list[len(lines_list) - 1] - int(image.height * 0.18), image.width, image.height))
    image1.save(fr'images/lines/{dir}/line22.png')


def cut_to_letters(dir, line):
    image = Image.open(fr'images/lines/{dir}/{line}')
    arr = np.array(image)
    list1 = [image.width - 1]  # A list in which the columns that are suspected as spaces are inserted
    for i in range(image.width - 1, 0, -1):  # From right to left because of the order in Hebrew letters
        counter = 0  # Counts the number of black pixels in a column
        for j in range(image.height):
            if arr[j][i].any() == 0:  # If the pixel is black
                counter += 1
        if (counter / image.height) > 0.042:
            list1.append(i)
    list2 = [list1[0]]  # List of pixel columns of beginning and end of a letter in a line
    for i in range(1, len(list1) - 1):
        if (list1[i + 1] - list1[i]) < -1:
            list2.append(list1[i])
    num_line = os.path.splitext(line)[0]
    os.makedirs(fr'images/letters/{dir}/{num_line}')
    for i in range(len(list2) - 1):  # Crop the letters from the line
        image1 = image.crop((list2[i + 1], 0, list2[i], image.height))
        image1.save(fr'images/letters/{dir}/{num_line}/letter{i}.png')
    image1 = image.crop((0, 0, list2[len(list2) - 1], image.height))
    image1.save(fr'images/letters/{dir}/{num_line}/letter{len(list2)}.png')





def main_separation_to_lines(path):
    path_to_my_lines = cut_lines(path)
    if len(os.listdir(path_to_my_lines)) == 21:
        dir = os.path.split(path_to_my_lines)[1]
        cut_line_21(dir, 'line21.png')
    return path_to_my_lines


def main_separation_to_letters(path):
    dir = os.path.split(path)[1]
    for line in os.listdir(path):
        if line.endswith('.jpg') or line.endswith('.png') or line.endswith('.PNG'):
           cut_to_letters(dir, line)

    return fr'images/letters/{dir}'

