import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox
from os.path import expanduser
from logging import getLogger

from PIL import Image, ImageTk, ImageEnhance, ImageOps
from cv2 import cv2
from numpy import array

from .rectangle import Rectangle
from .vertex import Vertex

logger = getLogger(__name__)


#
# class LookUpTable(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent)
#
#         img = cv2.imread(join(STATIC_DIR, 'request.jpg'))  # 画像の読み出し
#         img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # BGRからHSVに変換
#         h, s, v = cv2.split(img_hsv)  # チャンネルごとに分割
#
#         # ルックアップテーブルの生成
#         gamma = 2
#         look_up_table = zeros((256, 1), dtype=uint8)
#         for i in range(256):
#             look_up_table[i][0] = (i / 255) ** (1.0 / gamma) * 255
#
#         s_lut = cv2.LUT(s, look_up_table)  # 彩度(S)に対してルックアップテーブル適用
#         img_merge = cv2.merge([h, s_lut, v])  # H,変換後S,Vをマージ
#         img_bgr = cv2.cvtColor(img_merge, cv2.COLOR_HSV2BGR)  # HSVからBGRに変換
#
#         self.figure = plt.Figure()
#
#         ax1 = self.figure.add_subplot(221)
#         ax1.plot(x1, y1)
#         ax1.set_title('line plot')
#         ax1.set_ylabel('Damped oscillation')
#
#         # # ax2
#         # ax2 = self.figure.add_subplot(222)
#         # ax2.scatter(x1, y1, marker='o')
#         # ax2.set_title('Scatter plot')
#         #
#         # # ax3
#         # ax3 = self.figure.add_subplot(223)
#         # ax3.plot(x2, y2)
#         # ax3.set_ylabel('Damped oscillation')
#         # ax3.set_xlabel('time (s)')
#         #
#         # # ax4
#         # ax4 = self.figure.add_subplot(224)
#         # ax4.scatter(x2, y2, marker='o')
#         # ax4.set_xlabel('time (s)')
#
#         self.canvas = FigureCanvasTkAgg(self.figure, master=self)  # Generate canvas instance, Embedding fig in root
#         self.canvas.draw()
#         self.canvas.get_tk_widget().pack()


class ImageViewer(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.__touch_count = 0
        self.__rectangle = Rectangle(Vertex(0, 0), Vertex(0, 0))
        self.__real_rectangle = Rectangle(Vertex(0, 0), Vertex(0, 0))

        self.__original_image = None
        self.__attach_image = None
        self.__image_tk = None
        self.__display_image = None

        self.contrast_value = 1.00
        self.color_value = 1.00
        self.brightness_value = 1.00
        self.sharpness_value = 1.00
        self.rotate_angle = 0

        # region 画像表示
        self.canvas = tk.Canvas(bg='black', width=640, height=720)
        self.canvas.bind('<ButtonPress-1>', self.on_clicked_view)
        self.canvas.pack(side=tk.LEFT, anchor=tk.NW)
        # endregion

        # region 操作系
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y)

        # region ファイル操作
        self.file_control_frame = tk.Frame(self.control_frame)
        self.file_control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.select_new_image_button = tk.Button(
            self.file_control_frame,
            text='Select New Image',
            command=self.on_clicked_select_new_image_button
        )
        self.select_new_image_button.pack(side=tk.TOP, fill=tk.X)

        self.delete_button = tk.Button(
            self.file_control_frame,
            text='Delete',
            command=self.on_clicked_delete_button
        )
        self.delete_button.pack(side=tk.TOP, fill=tk.X)

        self.save_button = tk.Button(
            self.file_control_frame,
            text='Save',
            command=self.on_clicked_save_button
        )
        self.save_button.pack(side=tk.TOP, fill=tk.X)
        # endregion

        # region 画像処理
        # 画像保存ボタン
        self.image_control_frame = tk.Frame(self.control_frame, bg='purple')
        self.image_control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.rotate_button = tk.Button(
            self.image_control_frame,
            text='Rotate',
            command=self.on_clicked_rotate_button
        )
        self.rotate_button.pack(side=tk.TOP, fill=tk.X)

        self.crop_button = tk.Button(
            self.image_control_frame,
            text='Crop',
            command=self.on_clicked_crop_button
        )
        self.crop_button.pack(side=tk.TOP, fill=tk.X)

        self.process_buttons_frame = tk.Frame(self.control_frame, bg='purple')
        self.process_buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.reset_image_button = tk.Button(
            self.process_buttons_frame,
            text='Reset',
            command=self.on_clicked_reset_button
        )
        self.reset_image_button.pack(side=tk.TOP, fill=tk.X)

        self.contrast_scale_slider = tk.Scale(
            self.process_buttons_frame,
            orient=tk.HORIZONTAL,
            label='Contrast',
            from_=0.00,
            to=255.00,
            resolution=0.01,
            digits=5,
            command=self.on_changed_contrast
        )
        self.contrast_scale_slider.pack(side=tk.TOP, fill=tk.X)

        self.color_scale_slider = tk.Scale(
            self.process_buttons_frame,
            orient=tk.HORIZONTAL,
            label='Color',
            from_=0.00,
            to=255.00,
            resolution=0.01,
            digits=5,
            command=self.on_changed_color
        )
        self.color_scale_slider.pack(side=tk.TOP, fill=tk.X)

        self.brightness_scale_slider = tk.Scale(
            self.process_buttons_frame,
            orient=tk.HORIZONTAL,
            label='Brightness',
            from_=0.00,
            to=255.00,
            resolution=0.01,
            digits=5,
            command=self.on_changed_brightness
        )
        self.brightness_scale_slider.pack(side=tk.TOP, fill=tk.X)

        self.sharpness_scale_slider = tk.Scale(
            self.process_buttons_frame,
            orient=tk.HORIZONTAL,
            label='Sharpness',
            from_=0.00,
            to=255.00,
            resolution=0.01,
            digits=5,
            command=self.on_changed_sharpness
        )
        self.sharpness_scale_slider.pack(side=tk.TOP, fill=tk.X)

        label = tk.Label(self.process_buttons_frame, text='Channel', anchor=tk.W)
        label.pack(side=tk.TOP, fill=tk.X)
        self.chanel_control = Combobox(self.process_buttons_frame, values=self.chanel_control_patterns)
        self.chanel_control.set(self.chanel_control_patterns[0])
        self.chanel_control.bind('<<ComboboxSelected>>', self.on_changed_channel_control)
        self.chanel_control.pack(side=tk.TOP, fill=tk.X)
        # endregion

        # endregion
        self.initialize_image()
        self.initialize_cropping()
        self.reset()
        self.enable(is_enable=False)

        # self.look_up_table = LookUpTable(self)
        # self.look_up_table.pack(side=tk.LEFT, anchor=tk.NW)

    def initialize_image(self):
        self.__original_image: Image = Image.new('RGB', (500, 500), (0, 0, 0))
        self.redraw()

    def initialize_cropping(self):
        self.__touch_count = 0
        self.__rectangle = Rectangle(Vertex(0, 0), Vertex(0, 0))
        self.__real_rectangle = Rectangle(Vertex(0, 0), Vertex(0, 0))

    @property
    def original_image(self) -> Image:
        """オリジナルの画像.
        基本的にあらゆる編集を行わない.

        Returns: Union[Image, None]
        """
        return self.__original_image.copy()

    @original_image.setter
    def original_image(self, value: Image) -> None:
        self.__original_image = value

    @property
    def can_cropping(self) -> bool:
        return self.__touch_count != 0 and self.__touch_count % 2 == 0

    @property
    def cropping_image(self):
        image = self.original_image
        if self.can_cropping:
            image = image.crop(self.__real_rectangle.cropping_tuple)
        return image

    @property
    def processed_image(self):
        image = self.original_image

        contrast = ImageEnhance.Contrast(image)
        image = contrast.enhance(self.contrast_value)

        color = ImageEnhance.Color(image)
        image = color.enhance(self.color_value)

        brightness = ImageEnhance.Brightness(image)
        image = brightness.enhance(self.brightness_value)

        sharpness = ImageEnhance.Sharpness(image)
        image = sharpness.enhance(self.sharpness_value)

        selected = self.chanel_control.get()
        if selected != self.chanel_control_patterns[0]:
            image = ImageOps.grayscale(image)

        if selected == self.chanel_control_patterns[2]:
            array_image = array(image)
            th, array_image = cv2.threshold(array_image, 128, 192, cv2.THRESH_OTSU)
            image = Image.fromarray(array_image)
        elif selected == self.chanel_control_patterns[3]:
            array_image = array(image)
            th, array_image = cv2.threshold(array_image, 128, 192, cv2.THRESH_TRIANGLE)
            image = Image.fromarray(array_image)
        return image

    def redraw(self):
        self.canvas.delete('display')
        self.canvas.delete('rectangle')
        self.set_display_image(self.processed_image)

    def set_display_image(self, value: Image) -> None:
        w, h = value.size
        if w < h:
            resize = (int(w * (640 / h)), int(h * (720 / h)))
        else:
            resize = (int(w * (640 / w)), int(h * (720 / w)))

        self.__display_image = value.resize(resize)
        self.__image_tk = ImageTk.PhotoImage(image=self.__display_image)
        self.__attach_image = self.canvas.create_image(
            320 - (w * (640 / h) / 2) if w < h else 0,
            0 if w < h else 360 - (h * (720 / w) / 2),
            image=self.__image_tk,
            anchor=tk.NW,
            tag='display',
        )
        self.initialize_cropping()

    def enable(self, is_enable: bool = True):
        state = tk.NORMAL if is_enable else tk.DISABLED
        self.delete_button.config(state=state)
        self.reset_image_button.config(state=state)
        self.rotate_button.config(state=state)
        self.crop_button.config(state=state)
        self.save_button.config(state=state)
        self.contrast_scale_slider.config(state=state)
        self.color_scale_slider.config(state=state)
        self.brightness_scale_slider.config(state=state)
        self.sharpness_scale_slider.config(state=state)
        self.chanel_control.config(state=state)

    def reset(self):
        self.contrast_scale_slider.set(1.00)
        self.color_scale_slider.set(1.00)
        self.brightness_scale_slider.set(1.00)
        self.sharpness_scale_slider.set(1.00)
        self.chanel_control.set(self.chanel_control_patterns[0])
        self.redraw()

    def on_clicked_view(self, event):
        w, h = self.processed_image.size
        if w < h:
            x = (event.x - ((640 - self.__display_image.width) / 2)) * h / 640
            y = event.y * h / 720
        else:
            x = event.x * w / 640
            y = (event.y - ((720 - self.__display_image.height) / 2)) * w / 720
        real = Vertex(x, y)
        reduced = Vertex(event.x, event.y)
        if self.__touch_count % 2 == 0:
            self.canvas.delete('rectangle')
            self.__rectangle.top_left = reduced
            self.__real_rectangle.top_left = real
        else:
            self.__rectangle.bottom_right = reduced
            self.__real_rectangle.bottom_right = real
            self.canvas.create_rectangle(
                *self.__rectangle.cropping_tuple,
                tags='rectangle', outline='green'
            )
        self.__touch_count += 1
        logger.debug(self.__rectangle)

    def on_clicked_select_new_image_button(self):
        file = filedialog.askopenfile(initialdir=__file__)
        if file:
            logger.info(f'File selected {file}')
            self.canvas.delete('display')
            image = Image.open(open(file.name, 'rb'))
            self.original_image = image
            self.redraw()
            # self.canvas.itemconfig(self.__attach_image, image=self.__image_tk)
            self.enable()

    def on_clicked_delete_button(self):
        self.initialize_image()
        self.initialize_cropping()
        self.enable(is_enable=False)

    def on_clicked_save_button(self):
        file = filedialog.asksaveasfilename(
            parent=self,
            title='Save image to...',
            initialdir=expanduser('~'),
            initialfile='vision_tester_image',
            defaultextension='.jpg',
            filetypes=[('JPEG', '.jpg'), ('PNG', '.png'), ('Bitmap', '.bmp'), ('Tiff', '.tif')]
        )
        if file:
            self.processed_image.save(file, quality=100)
        else:
            # TODO: SnackMessage
            logger.debug('Cancel file save')

    def on_clicked_reset_button(self):
        self.reset()

    def on_clicked_rotate_button(self):
        self.original_image = self.original_image.rotate(90, expand=True)
        self.redraw()

    def on_clicked_crop_button(self):
        self.canvas.delete('rectangle')
        self.original_image = self.cropping_image
        self.initialize_cropping()
        self.redraw()

    def on_changed_contrast(self, value):
        self.contrast_value = float(value)
        self.redraw()

    def on_changed_color(self, value):
        self.color_value = float(value)
        self.redraw()

    def on_changed_brightness(self, value):
        self.brightness_value = float(value)
        self.redraw()

    def on_changed_sharpness(self, value):
        self.sharpness_value = float(value)
        self.redraw()

    chanel_control_patterns = [
        'None',
        'grayscale',
        'grayscale + Bitwise(Otsu)',
        'grayscale + Bitwise(Triangle)'
    ]

    def on_changed_channel_control(self, event):
        self.redraw()
