
import os
import os.path
from PIL import Image
'''
filein: 输入图片
fileout: 输出图片
width: 输出图片宽度
height:输出图片高度
type:输出图片类型（png, gif, jpeg...）
'''
def ResizeImage(filein, fileout, width, height, type):
  img = Image.open(filein)
  out = img.resize((width, height),Image.ANTIALIAS)
  #resize image with high-quality
  out.save(fileout)
if __name__ == "__main__":
  filein = r'img.jpg'
  fileout = r'img-1.jpg'
  width = 150
  height = 200
  type = 'jpg'
  ResizeImage(filein, fileout, width, height, type)
