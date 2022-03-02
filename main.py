from tkinter import Tk
from logging import getLogger
from app import VisionTester

logger = getLogger(__name__)

if __name__ == '__main__':
    logger.debug('Running application')
    root = Tk()
    root.geometry('1280x720')
    root.resizable(False, False)
    root.title('Vision Tester')
    app = VisionTester(master=root)
    app.mainloop()

    logger.debug('Stop application')
