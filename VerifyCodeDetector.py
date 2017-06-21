import pytesseract

from PIL import Image

image = Image.open('/home/ubuntu/WebServer/verify.png')

vcode = pytesseract.image_to_string(image)

print (vcode)
