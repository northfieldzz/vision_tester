from os import environ
from platform import system
from io import open
from time import time
from logging import getLogger
from tkinter import (
    Frame,
    Button,
    LEFT,
    TOP,
    filedialog,
    StringVar,
    Label,
    Checkbutton,
    BooleanVar,
    Scrollbar,
    VERTICAL,
    Text,
    RIGHT
)

from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision

from components.environment import STATIC_DIR

logger = getLogger(__name__)


class Control(Frame):
    @property
    def font(self):
        if system() == 'Windows':
            return ImageFont.truetype(f'C:/Windows/Fonts/msgothic.ttc', 15)
        else:
            return ImageFont.truetype(f'{STATIC_DIR}/SourceHanSans-VF.otf.ttc', 15)

    def __init__(self, master, image_view):
        super().__init__(master)
        self.image_view = image_view

        frame_1 = Frame(self)
        self.auth_file = StringVar()
        label = Label(frame_1, textvariable=self.auth_file)
        label.pack(side=LEFT, expand=True)
        button = Button(frame_1, text='Auth file', command=self.button_pressed_select_auth_file)
        button.pack(side=RIGHT)
        frame_1.pack(fill='x')

        frame_2 = Frame(self)
        self.boolean_var = BooleanVar()
        self.boolean_var.set(False)
        checkbox = Checkbutton(frame_2, variable=self.boolean_var, text="Language Hints=['kr']")
        checkbox.pack(side=LEFT)
        button = Button(frame_2, text="Request", command=self.button_pressed_request)
        button.pack(side=RIGHT)
        frame_2.pack(fill='x')

        frame_3 = Frame(self)
        ybar = Scrollbar(self, orient=VERTICAL)
        self.result_widget = Text(frame_3)
        self.result_widget.pack(side=TOP)
        self.result_widget.config(yscrollcommand=ybar.set)
        ybar.config(command=self.result_widget.yview)
        frame_3.pack(fill='both', expand=True)

    def button_pressed_select_auth_file(self):
        file = filedialog.askopenfile(initialdir=__file__)
        if file:
            environ["GOOGLE_APPLICATION_CREDENTIALS"] = file.name
            filename = file.name
            if len(filename) > 30:
                filename = f'...{filename[-30:]}'
            self.auth_file.set(filename)

    def button_pressed_request(self):
        self.image_view.original_image.save(f'{STATIC_DIR}/request.jpg', quality=100)
        client = vision.ImageAnnotatorClient()

        with open(f'{STATIC_DIR}/request.jpg', 'rb') as image_file:
            content = image_file.read()

        image = vision.Image({'content': content})

        image_context = vision.ImageContext()
        if self.boolean_var.get():
            image_context.language_hints = ['kr']
        else:
            image_context.language_hints = ['ja-t-i0-handwrit']
        response = client.text_detection(
            image=image,
            image_context=image_context
        )
        img = Image.open(f'{STATIC_DIR}/request.jpg')
        draw = ImageDraw.Draw(img)
        texts = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            box = [(vertex.x, vertex.y) for vertex in symbol.bounding_box.vertices]
                            draw.line(box + [box[0]], width=2, fill='#00ff00')
                            draw.text((symbol.bounding_box.vertices[0].x, symbol.bounding_box.vertices[0].y - 20),
                                      symbol.text,
                                      font=self.font,
                                      fill='#FF0000')
                            texts.append(symbol.text)
        draw.text((200, 200), ''.join(texts), font=self.font, fill='#FF0000')
        self.result = response
        if response.error.message:
            raise Exception(f'{response.error.message}\n'
                            f'For more info on error messages, check: https://cloud.google.com/apis/design/errors')
        img.save(f'{STATIC_DIR}/result_{time()}.jpg', quality=100)
        self.image_view.original_image = img

    @property
    def result(self):
        return self.result_widget.get('1.0', 'end -1c')

    @result.setter
    def result(self, response):
        self.result_widget.delete('1.0', 'end')
        result_sentence = ''
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                result_sentence += f'\nBlock confidence: {block.confidence}'
                for paragraph in block.paragraphs:
                    result_sentence += f'\n  Paragraph confidence: {paragraph.confidence}'
                    for word in paragraph.words:
                        context = ''.join([symbol.text for symbol in word.symbols])
                        result_sentence += f"\n    Word text: {context} (confidence: {word.confidence})"
        logger.debug(result_sentence)
        self.result_widget.insert('1.0', result_sentence)
