import tkinter as tk
from os import makedirs
from logging import getLogger
from gui.image_viewer import ImageViewer
from gui.log_viewer import LogViewer
from gui.log_viewer import stream_handler
from components.environment import STATIC_DIR

logger = getLogger(__name__)
logger.addHandler(stream_handler)

makedirs(STATIC_DIR, exist_ok=True)


class VisionTester(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.image_viewer = ImageViewer(self)
        self.image_viewer.pack(side=tk.LEFT, anchor=tk.NW)

        self.log_viewer = LogViewer(self)
        self.log_viewer.pack(side=tk.LEFT,
                             anchor=tk.NW,
                             fill=tk.BOTH)

        # self.control = Control(self, self.image_view)
        # self.control.pack(side=tk.LEFT, fill=tk.BOTH)
