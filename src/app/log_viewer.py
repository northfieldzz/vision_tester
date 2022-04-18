import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from io import StringIO
from logging import getLogger, StreamHandler, Formatter, INFO
from threading import Thread

logger = getLogger(__name__)

log_capture_io = StringIO()
stream_handler = StreamHandler(stream=log_capture_io)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(INFO)


class LogViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.log_window = ScrolledText(self, state=tk.DISABLED)
        self.log_window.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill=tk.BOTH)

        self._is_loop = True
        # self.thread = Thread(target=self.run)
        # self.thread.start()

    def write(self, text):
        self.log_window.config(state=tk.NORMAL)
        self.log_window.insert(tk.END, text)
        self.log_window.see(tk.END)
        self.log_window.config(state=tk.DISABLED)

    def run(self):
        while self._is_loop:
            print(log_capture_io.getvalue())
