from tkinter import (
    Frame,
    Button,
    Canvas,
    NW,
    W,
    LEFT,
    TOP,
    filedialog,
    StringVar,
    Entry,
    Checkbutton,
    BooleanVar,
)
import numpy as np
from PIL import Image, ImageTk, ImageEnhance, ImageOps

from cv2 import cv2

from . import STATIC_DIR


class ImageView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.attach_image = None
        self.touch_count = 0
        self.rectangle = [[0, 0], [0, 0]]
        self.real_rectangle = [[0, 0], [0, 0]]

        self.canvas = Canvas(bg='black', width=640, height=720)
        self.canvas.bind('<ButtonPress-1>', self.on_click_view)
        self.canvas.pack(side=LEFT)
        self.original_image = Image.open(open(f'{STATIC_DIR}/sample.jpg', 'rb'))

        self.file_select_button = Button(self, text='Image File', command=self.button_pressed_file_select)
        self.file_select_button.pack(side=TOP, fill='both')

        self.rotate_button = Button(self, text='Rotate', command=self.button_pressed_rotate)
        self.rotate_button.pack(side=TOP, fill='both')

        self.crop_button = Button(self, text='Crop', command=self.button_pressed_crop)
        self.crop_button.pack(side=TOP, fill='both')

        self.save_button = Button(self, text='Save', command=self.button_pressed_save)
        self.save_button.pack(side=TOP, fill='both')

        self.contrast_var = StringVar()
        self.contrast_var.set('1.0')
        entry = Entry(self, textvariable=self.contrast_var)
        entry.pack(side=TOP, fill='both', anchor=W)

        self.grayscale_var = BooleanVar()
        self.grayscale_var.set(False)
        checkbox = Checkbutton(self, variable=self.grayscale_var, text='GrayScale')
        checkbox.pack(side=TOP, fill='both', anchor=W)

        self.bitwise_var_otsu = BooleanVar()
        self.bitwise_var_otsu.set(False)
        checkbox = Checkbutton(self, variable=self.bitwise_var_otsu, text='Bitwise Otsu')
        checkbox.pack(side=TOP, fill='both', anchor=W)

        self.bitwise_var_triangle = BooleanVar()
        self.bitwise_var_triangle.set(False)
        checkbox = Checkbutton(self, variable=self.bitwise_var_triangle, text='Bitwise Triangle')
        checkbox.pack(side=TOP, fill='both', anchor=W)

        button = Button(self, text="Submit", command=self.button_pressed_submit)
        button.pack(side=TOP, fill='both', anchor=W)

    def on_click_view(self, event):
        if self.w < self.h:
            x = (event.x - ((640 - self.display_image.width) / 2)) * self.h / 640
            y = event.y * self.h / 720
        else:
            x = event.x * self.w / 640
            y = (event.y - ((720 - self.display_image.height) / 2)) * self.w / 720
        if self.touch_count % 2 == 0:
            self.canvas.delete('rectangle')
            self.real_rectangle[0] = [x, y]
            self.rectangle[0] = [event.x, event.y]
        else:
            self.real_rectangle[1] = [x, y]
            self.rectangle[1] = [event.x, event.y]
            self.canvas.create_rectangle(
                self.rectangle[0][0], self.rectangle[0][1],
                self.rectangle[1][0], self.rectangle[1][1],
                tag='rectangle', outline='green'
            )
        self.touch_count += 1
        print(self.rectangle)

    def button_pressed_rotate(self):
        self.canvas.delete('display')
        self.original_image = self.original_image.rotate(90, expand=True)
        self.canvas.itemconfig(self.attach_image, image=self.image_tk)

    @property
    def crop_image(self):
        if self.touch_count == 0 or self.touch_count % 2 != 0:
            return self.original_image

        return self.original_image.crop(
            (
                self.real_rectangle[0][0],
                self.real_rectangle[0][1],
                self.real_rectangle[1][0],
                self.real_rectangle[1][1]
            )
        )

    def button_pressed_crop(self):
        self.crop_image.save(f'{STATIC_DIR}/cropping.jpg', quality=100)
        self.original_image = self.crop_image

    def button_pressed_file_select(self):
        file = filedialog.askopenfile(initialdir=__file__)
        if file:
            self.canvas.delete('display')
            self.original_image = Image.open(open(file.name, 'rb'))
            self.canvas.itemconfig(self.attach_image, image=self.image_tk)

    def button_pressed_save(self):
        self.original_image.save(f'{STATIC_DIR}/result.jpg', quality=100)

    def button_pressed_submit(self):
        contrast = ImageEnhance.Contrast(self.original_image)
        image = contrast.enhance(float(self.contrast_var.get()))

        if self.grayscale_var.get() or self.bitwise_var_otsu.get() or self.bitwise_var_triangle.get():
            image = ImageOps.grayscale(image)

        if self.bitwise_var_otsu.get():
            array_image = np.array(image)
            th, array_image = cv2.threshold(array_image, 128, 192, cv2.THRESH_OTSU)
            image = Image.fromarray(array_image)
        elif self.bitwise_var_triangle.get():
            array_image = np.array(image)
            th, array_image = cv2.threshold(array_image, 128, 192, cv2.THRESH_TRIANGLE)
            image = Image.fromarray(array_image)
        self.original_image = image

    @property
    def original_image(self):
        return self._original_image

    @original_image.setter
    def original_image(self, value):
        self._original_image = value
        temp = self._original_image.copy()
        self.w, self.h = self._original_image.size

        if self.w < self.h:
            resize = (int(self.w * (640 / self.h)), int(self.h * (720 / self.h)))
        else:
            resize = (int(self.w * (640 / self.w)), int(self.h * (720 / self.w)))

        self.display_image = temp.resize(resize)
        self.image_tk = ImageTk.PhotoImage(image=self.display_image)
        self.attach_image = self.canvas.create_image(
            320 - (self.w * (640 / self.h) / 2) if self.w < self.h else 0,
            0 if self.w < self.h else 360 - (self.h * (720 / self.w) / 2),
            image=self.image_tk,
            anchor=NW,
            tag='display',
        )

        self.real_rectangle = [[0, 0], [0, 0]]
        self.rectangle = [[0, 0], [0, 0]]
        self.touch_count = 0
