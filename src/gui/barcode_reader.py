from tkinter import Frame, Canvas, filedialog, Button, BOTH, Label, NW
from PIL import Image, ImageTk

from components import barcode


class BarcodeReader(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        master.title('Barcode Reader')

        self.canvas = Canvas(self, bg='black')
        self.canvas.pack(expand=True, fill=BOTH)

        self.button = Button(
            self,
            text='ファイルダイアログを開く',
            font=('', 20),
            width=24,
            height=1,
            bg='#999999',
            activebackground='#aaaaaa'
        )
        self.button.bind('<ButtonPress>', self.show_dialog)
        self.button.pack()

        self.label = Label(self, text='', font=('', '20'))
        self.label.pack()

        self.set_image('./sample.jpeg')

    def set_image(self, path):
        image = Image.open(path)
        self.canvas.photo = ImageTk.PhotoImage(image)
        self._display()
        self.label['text'] = barcode.reader(image)

    def _display(self):
        photo = self.canvas.photo
        width = photo.width()
        if width > 1080:
            width = 1080
        height = photo.height()
        if height > 1080:
            height = 1080
        self.canvas.config(width=width, height=height)
        self.canvas.create_image(0, 0, anchor=NW, image=photo)

    def show_dialog(self, event) -> None:
        file_types = [
            ('Image', '*.png'),
            ('Image', '*.PNG'),
            ('Image', '*.jpg'),
            ('Image', '*.jpeg'),
            ('Image', '*.JPG')
        ]
        image_file = filedialog.askopenfilename(filetypes=file_types)
        self.set_image(image_file)
