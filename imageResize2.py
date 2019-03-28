import cv2

def main(_pathInputPic, _downscale):
    oriimg = cv2.imread(_pathInputPic)
    height, width, depth = oriimg.shape
    baseWidth = width / 3 * _downscale
    imgScale = baseWidth/width
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    oriimg = cv2.resize(oriimg, (int(newX), int(newY)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(_pathInputPic, oriimg)


##---------------------------------------------------------------------------------------------------------->
#Preferable interpolation methods are cv.INTER_AREA for shrinking and cv.INTER_CUBIC(slow) & cv.INTER_LINEAR
#for zooming. By default, interpolation method used is cv.INTER_LINEAR for all resizing purposes.
