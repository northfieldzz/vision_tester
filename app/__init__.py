from os import makedirs
from tkinter import Frame, NW, LEFT
from image_view import ImageView
from control import Control

STATIC_DIR = './static'
makedirs(STATIC_DIR, exist_ok=True)


class VisionTester(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.image_view = ImageView(self)
        self.image_view.pack(side=LEFT, anchor=NW, expand=True)

        self.control = Control(self, self.image_view)
        self.control.pack(side=LEFT)

        self.pack()
