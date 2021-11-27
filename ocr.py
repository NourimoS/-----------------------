import sys


import cv2.cv2 as cv
from os import rename

import numpy as np
import pytesseract


try:

    from PIL import Image, ImageDraw


except ImportError:

    import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\gabde\AppData\Local\Programs\Tesseract-OCR\tesseract'

rect_header_right = (540, 50, 880, 90)
rect_header_left = (70, 50, 415, 90)
rect_left = (50, 90, 524, 830)
rect_right = (426, 90, 900, 830)
thresh = 200
amt = 50
fileRange = range(9, 613)


lambda x: x-amt if x < thresh else 255


def transformImages():

    for x in fileRange:

        name = str(x).rjust(3, '0')

        image = Image.open(f"org/{name}.jpeg")

        image = image.convert('L').point(fn, mode='L')

        draw = ImageDraw.Draw(image)

        draw.rectangle(rect_header_right if x %


                       2 else rect_header_left, fill="white")

        draw.rectangle(rect_right if not x % 2 else rect_left, fill="white")

        image.save(f"bnw/{name}_bw.jpeg")

    print('finished')


# transformImages()


def getYposes(nidle, page, t):

    nidle = cv.imread(nidle)

    nw, nh, _ = nidle.shape

    result = cv.matchTemplate(page, nidle, cv.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(result >= t)

    rectangles = []

    for (x, y) in zip(xloc, yloc):

        r = (int(x), int(y), int(nw), int(nh))

        rectangles.append(r)

        rectangles.append(r)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.2)

    rectangles_y = [y for (x, y, w, h) in rectangles]

    rectangles_y = list(dict.fromkeys(rectangles_y))

    return rectangles_y


def renameFiles():

    path = r"C:\Users\gabde\Documents\المختصر في تفسير القرآن\bnw"

    suffix = "_bw.jpeg"

    for x in fileRange:

        n = x-8

        name = str(x).rjust(3, '0')

        newName = str(n).rjust(3, '0')

        src = path+"\\{name+suffix}"

        dst = f"{path}\\{newName+suffix}"

        rename(src, dst)

    print("done")


def linePages(p):
    page = rf"bnw\\{p}_bw.jpeg"
    page = cv.imread(page)
    aye_stop = r"samples\aye_stop.jpg"
    # section_stop = r"samples\section_stop.jpg"
    foaid_section = r"samples\foaid_section.jpg"
    surah_start = r"samples\surah_start.jpg"
    quron_preview = r"samples\aye_frame.jpg"
    # sections = getYposes(section_stop, page, 0.75)
    # foaid = getYposes(foaid_section, page, 0.6)
    # print(foaid)
    suraas = getYposes(surah_start, page, 0.8)
    ayes = getYposes(aye_stop, page, 0.55)
    # cv.line(page, (0, foaid[0]), (page.shape[1], foaid[0]), (255, 0, 0), 2)
    # for y in sections:
    #     cv.line(page, (0, y), (page.shape[1], y), (255, 0, 0), 2)
    for y in suraas:
        cv.line(page, (0, y), (page.shape[1], y), (0, 255, 0), 2)
    for y in ayes:
        cv.rectangle(page, (0, y), (page.shape[1], y), (0, 0, 255), 2)
    filename = fr"lined\\{p}.jpeg"
    cropedPage = page[0: ayes[0], page.shape[1]:ayes[1]]
    cv.imshow("Display window", cropedPage)
    cv.waitKey()
    cv.destroyAllWindows()
    # cv.imwrite(filename, page)


# fileRange = range(1, 604)
# for x in fileRange:
#     fileName = str(x).rjust(3, "0")
    # linePages(fileName)
linePages(511)
