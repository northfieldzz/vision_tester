from pyzbar import pyzbar
import numpy as np


def reader(image: np.array) -> str:
    data = pyzbar.decode(np.array(image))
    return data[0][0].decode('utf-8', 'ignore') if data else "Unreadable"
