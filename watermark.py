from PIL import Image
from io import BytesIO
import base64

def watermark_with_transparency(input_image, watermark_image_path):
    base_image = input_image.convert("RGBA") # convert to RGBA is important
    watermark = Image.open(watermark_image_path).convert("RGBA")
    width, height = base_image.size
    mark_width, mark_height = watermark.size
    #position = (width-mark_width,height-mark_height) # put the watermark at the lower-right corner
    position = (int((width/2) - (mark_width/2)), int((height/2) - (mark_height/2))) # put the watermark at the middle
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    transparent.paste(watermark, position, mask=watermark)
    buff = BytesIO()
    transparent.save(buff, format="PNG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return new_image_string


######################################################

##usage:

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<
            #del ioFile
            #downloadFile2xSize()
            #img = upscale2.main(img, PATH_TO_SCALE_FILE + '2xSize.pth')
            #img = imageResize2.main2(img) #--> 1/3 downscale
            #img = Image.fromarray(img)#.astype("uint8")
            #rawBytes = BytesIO()
            #img.save(rawBytes, format='PNG') #JPEG
            #rawBytes.seek(0)
            #img_s = base64.b64encode(rawBytes.read()).decode()
            #saveBase64StringToFile('s', img_s)
            #img_w = watermark.watermark_with_transparency(img, '/home/gexvo/mySite_WebApp/assets/otherStuff/watermark.png')

            #img_show = img_w #or img_s
