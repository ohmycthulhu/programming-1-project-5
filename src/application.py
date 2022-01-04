import tkinter as tk
import os
from PIL import Image, ImageTk
import pdf2image
from src.scrollable_image import ScrollableImage
from src.mind_map_controller import MindMapController


class Application(tk.Tk):
    """
        Class representing the whole application.
        It manages the windows, allows creating new windows for displaying images,
        and also can convert PDF files into images.
    """
    DATA_DIR = './data'
    TMP_DIR = './tmp'
    IMAGE_WIDTH = 720
    IMAGE_HEIGHT = 720

    def __init__(self, title='No name', maps=None, **kwargs):
        if maps is None:
            maps = []
        super(Application, self).__init__(**kwargs)
        self.title(title)
        self._mm = MindMapController(maps)
        self._construct()

    @staticmethod
    def _read_files():
        return os.listdir(Application.DATA_DIR)

    def _construct(self):
        current_row = 0

        # Mind map button
        tk.Button(self, text='Show combined mind map', command=self._display_mind_map)\
            .grid(row=current_row, column=0, columnspan=2)
        current_row += 1

        # Images show section
        tk.Label(master=self, text='Available Files')\
            .grid(row=current_row, column=0, columnspan=2)
        current_row += 1

        files = self._read_files()
        for i, file in enumerate(files):
            tk.Button(self, text=file, command=lambda f=file: self._display_image(f))\
                .grid(row=int(current_row), column=(i % 2))
            current_row += 1 / 2
        current_row += 1  # It's not necessary, but looks more consistent

    def _display_mind_map(self):
        path = 'tmp/mind_map.png'
        # if not os.path.exists(path):
        self._mm.export(path)
        self._display_local_image(path, title='Mind Map')

    @staticmethod
    def _display_image(file_name):
        path = Application._convert_if_needed(os.path.join(Application.DATA_DIR, file_name))
        Application._display_local_image(path, file_name)

    @staticmethod
    def _display_local_image(path, title):
        # Create new window with only one widget (Image to show)
        w = tk.Tk()
        w.title(title)

        # Load image and initialize widget
        load = Image.open(path)
        img = ImageTk.PhotoImage(load, master=w)
        ScrollableImage(master=w, image=img, width=Application.IMAGE_WIDTH, height=Application.IMAGE_HEIGHT).pack()

        w.mainloop()

    @staticmethod
    def _convert_if_needed(full_path):
        # Extract file name, extension, and name without the extension
        file_name_with_extension = os.path.split(full_path)[-1]
        parts = file_name_with_extension.split('.')
        file_name, ext = '.'.join(parts[:-1]), parts[-1]

        # Continue only if file is PDF
        if ext.lower() != 'pdf':
            return full_path

        # Convert only the first image as jpg file
        images = pdf2image.convert_from_path(full_path)

        if len(images) == 0:
            raise Exception(f"Failed to convert {full_path} into image")

        new_path = os.path.join(Application.TMP_DIR, f"{file_name}.jpg")

        images[0].save(new_path, 'JPEG')

        return new_path
