import tkinter as tk
import os
from PIL import Image, ImageTk
import pdf2image
from src.scrollable_image import ScrollableImage


class Application(tk.Tk):
    DATA_DIR = './data'
    TMP_DIR = './tmp'

    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        self._construct()

    @staticmethod
    def _read_files():
        return os.listdir(Application.DATA_DIR)

    def _construct(self):
        files = self._read_files()
        for file in files:
            tk.Button(self, text=file, command=lambda f=file: self._display_image(f)).pack()

    @staticmethod
    def _display_image(file_name):
        w = tk.Tk()
        w.title(file_name)
        path = Application._convert_if_needed(os.path.join(Application.DATA_DIR, file_name))
        load = Image.open(path)
        img = ImageTk.PhotoImage(load, master=w)
        ScrollableImage(master=w, image=img, width=600, height=600).pack()

        w.mainloop()

    @staticmethod
    def _convert_if_needed(full_path):
        file_name_with_extension = os.path.split(full_path)[-1]
        parts = file_name_with_extension.split('.')
        file_name, ext = '.'.join(parts[:-1]), parts[-1]

        if ext.lower() != 'pdf':
            return full_path

        images = pdf2image.convert_from_path(full_path)

        if len(images) == 0:
            raise Exception(f"Failed to convert {full_path} into image")

        new_path = os.path.join(Application.TMP_DIR, f"{file_name}.jpg")

        images[0].save(new_path, 'JPEG')

        return new_path
