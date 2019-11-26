# Author: Jordan Chapman

from pygameFunctions import *
from Test.BasicSprite import BasicSprite


class Text(BasicSprite):
    def __init__(self, text, x, y, size, text_color):
        self.font = pygame.font.Font(None, size)
        self._text = text
        self.text_color = text_color
        super(Text, self).__init__(x=x, y=y, image=self.update_text())

    def update_text(self):
        return self.font.render(self._text, 1, self.text_color)

    def get_text(self):
        return self._text

    def set_text(self, text):
        if text != self._text:
            self._text = text
            self.set_image(self.update_text())

    text = property(get_text, set_text)