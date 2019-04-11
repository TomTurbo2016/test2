from cv2 import imread, imdecode, resize, imwrite, IMREAD_COLOR, INTER_AREA
import numpy as np


def main2(baseWidth, imageBytes):
    npArr = np.asarray(bytearray(imageBytes.read()), dtype=np.uint8)
    oriimg = imdecode(npArr, IMREAD_COLOR)
    height, width, depth = oriimg.shape
    if width > baseWidth or height > baseWidth:
        if height >= width:
            imgScale = baseWidth/width
            newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
            oriimg = resize(oriimg, (int(newX), int(newY)), interpolation=INTER_AREA)
        else:
            imgScale = baseWidth/height
            newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
            oriimg = resize(oriimg, (int(newX), int(newY)), interpolation=INTER_AREA)
        return oriimg
    else:
        return oriimg
