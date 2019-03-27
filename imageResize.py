import cv2

def main(baseWidth, pathInputPic):
    oriimg = cv2.imread(pathInputPic)
    height, width, depth = oriimg.shape
    if width > baseWidth or height > baseWidth:
        if height >= width:
            imgScale = baseWidth/width
            newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
            oriimg = cv2.resize(oriimg, (int(newX), int(newY)), interpolation=cv2.INTER_AREA)
        else:
            imgScale = baseWidth/height
            newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
            oriimg = cv2.resize(oriimg, (int(newX), int(newY)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(pathInputPic, oriimg)


##---------------------------------------------------------------------------------------------------------->
#Preferable interpolation methods are cv.INTER_AREA for shrinking and cv.INTER_CUBIC(slow) & cv.INTER_LINEAR
#for zooming. By default, interpolation method used is cv.INTER_LINEAR for all resizing purposes.
