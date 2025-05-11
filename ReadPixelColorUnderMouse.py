#python3 -m pip install --upgrade Pillow
import ctypes
import pyautogui
from PIL import ImageGrab
import time

# Constants
SRCCOPY = 0xCC0020

# Function to get pixel color using ctypes and Gdi32 library
def get_pixel_color_ctypes(x, y):
    user32 = ctypes.windll.user32
    hdc = user32.GetDC(0)
    gdi32 = ctypes.windll.gdi32
    pixel = gdi32.GetPixel(hdc, x, y)
    user32.ReleaseDC(0, hdc)
    rgb = (pixel & 0xff, (pixel >> 8) & 0xff, (pixel >> 16) & 0xff)
    return rgb

# Function to get pixel color using ImageGrab
def get_pixel_color_imagegrab(x, y):
    screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    color = screenshot.getpixel((0, 0))
    return color

# Function to continuously display pixel color
def display_pixel_color():
    while True:
        x, y = pyautogui.position()

        # Using ctypes and Gdi32
        color_ctypes = get_pixel_color_ctypes(x, y)
        print("Using ctypes and Gdi32 - Color at ({}, {}): {}".format(x, y, color_ctypes))

        # Using ImageGrab
        color_imagegrab = get_pixel_color_imagegrab(x, y)
        print("Using ImageGrab - Color at ({}, {}): {}".format(x, y, color_imagegrab))

        pct_x = color_ctypes[0] /255.0*100.0
        pct_y = color_ctypes[1] /255.0*100.0
        pct_z = color_ctypes[2] /255.0*360.0
        print("Test wow  ({}, {}): {}% {}% {}%".format(x, y, pct_x, pct_y, pct_z))

        time.sleep(1)

if __name__ == "__main__":
    display_pixel_color()
