from os import path
from tkinter import Tk
from logging import getLogger
from gui import VisionTester
from components import environment

logger = getLogger(__name__)

if __name__ == '__main__':
    icon_file = path.join(environment.STATIC_DIR, 'icons', 'logos.ico')
    logger.debug('Running application')
    root = Tk()
    # root.geometry('1280x720')
    # root.resizable(False, False)
    root.title('Vision Tester')
    root.iconbitmap(default=icon_file)
    app = VisionTester(master=root)
    app.pack()
    app.mainloop()

    logger.debug('Stop application')
