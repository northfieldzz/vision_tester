from tkinter import Tk
from app import VisionTester

if __name__ == '__main__':
    root = Tk()
    root.geometry('1280x720')
    root.resizable(width=0, height=0)
    root.title('Vision Tester')
    app = VisionTester(master=root)
    app.mainloop()
