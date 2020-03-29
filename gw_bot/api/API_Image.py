import base64
import io

from PIL import Image, ImageFont, ImageDraw

from osbot_utils.utils.Files import temp_file

# uses PILlOW api (https://pypi.org/project/Pillow/)
# See more examples at:
# - https://code-maven.com/create-images-with-python-pil-pillow
# - http://www.blog.pythonlibrary.org/2017/10/17/how-to-watermark-your-photos-with-python/
# - https://pillow.readthedocs.io/en/latest/handbook/tutorial.html#reading-and-writing-images
# - http://effbot.org/imagingbook/introduction.htm

class API_Image:
    def __init__(self, img_file=None):
        self.img_file = img_file
        self.image    = None

    def add_text(self, text, top=0, left=0, color='black'):
        if self.image:
            drawing = ImageDraw.Draw(self.image)
            font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)  # todo: remove hard-coded reference
            drawing.text((top,left), text, fill=color, font=font)
        return self

    def info(self):
        result = {}
        if self.image is None:
            result['error'] = 'no image'
        else:
            (width,height)   = self.image.size
            result['width' ] = width
            result['height'] = height
        return result

    def new_rgb(self, mode="RGB", width=200, height=70,color='white'):
        self.image = Image.new(mode=mode, size=(width, height), color=color)
        return self

    def load_from_bytes_base64(self, png_data):
        png_bytes = base64.decodebytes(png_data.encode())
        return self.new_from_bytes(png_bytes)

    def new_from_bytes(self, png_bytes):
        self.image = Image.open(io.BytesIO(png_bytes))
        return self

    def save(self):
        if self.img_file is None:
            self.img_file = temp_file(extension='.png')
        if self.image is not None:
            self.image.save(self.img_file)
        return self

    def set_img_file(self, img_file):
        self.img_file = img_file
        return self





