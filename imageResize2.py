from cv2 import imread, resize, imwrite, INTER_AREA
from PIL import Image
import numpy as np


def main2(_img):
    width, height = _img.size
    pic = _img.resize((int(width / 4 * 3), int(height / 4 * 3)), Image.LANCZOS)
    return np.array(pic)
