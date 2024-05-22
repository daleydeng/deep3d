import numpy as np
from PIL import ImageDraw, Image, ImageFont

class TextDraw:
    def __init__(self, size=20):
        self.size = size
        self.font = ImageFont.truetype('SourceHanSansCN-Light', size)

    def draw(self, img, txt, xy, **kws):
        img = Image.fromarray(img)
        d = ImageDraw.Draw(img)
        d.text(xy, txt, font=self.font, **kws)
        return np.array(img, dtype='u1')
