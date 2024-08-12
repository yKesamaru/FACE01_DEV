"""Example: 簡易ファイルラウザ実装例

Summary:
    ttkbootstrapを用いた簡易ファイルブラウザ実装例

Example:
    .. code-block:: bash

        python3 example/simple_file_browser.py

See also:
    ttkbootstrap
    https://ttkbootstrap.readthedocs.io/en/version-0.5/themes.html

"""

import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from ttkbootstrap import Style  # type: ignore


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("preset_face_images")
        self.geometry("800x600")
        self.resizable(True, True)
        self.style = Style(theme="minty")
        self.style.configure("TButton", font=("Arial", 12))


class ImageBrowser:
    def __init__(self, master, path):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill="both", expand=True)

        self.image_list = []
        self.load_images(path)

        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind('<Configure>', self.on_configure)
        self.canvas_frame.bind_all('<MouseWheel>', self.on_mousewheel)

        self.photos = []

        self.image_label = ttk.Label(self.frame)
        self.image_label.pack(fill="both", expand=True)

        self.current_image_path = None
        if self.image_list:
            self.current_image_path = self.image_list[0]
            self.master.after(100, self.show_image, self.current_image_path)

    def load_images(self, path):
        for file_name in os.listdir(path):
            if file_name.endswith(('.png', '.jpg', '.jpeg')):
                self.image_list.append(os.path.join(path, file_name))

    def on_configure(self, event):
        self.canvas.delete('all')
        self.photos = []
        x = 10
        y = 10
        thumbnail_width = 100
        thumbnail_height = 100
        for image_path in self.image_list:
            img = Image.open(image_path)
            img.thumbnail((thumbnail_width, thumbnail_height))
            photo = ImageTk.PhotoImage(img)
            self.photos.append(photo)

            image_id = self.canvas.create_image(x, y, image=photo, anchor='nw')
            self.canvas.tag_bind(image_id, '<Double-Button-1>',
                                 lambda e, path=image_path: self.show_image(path))

            x += thumbnail_width + 10
            if x > event.width - thumbnail_width:
                x = 10
                y += thumbnail_height + 10

        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        if self.current_image_path:
            self.show_image(self.current_image_path)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def show_image(self, image_path):
        self.current_image_path = image_path
        img = Image.open(image_path)
        img.thumbnail((self.master.winfo_width(), max(
            1, self.master.winfo_height() // 2)))
        photo = ImageTk.PhotoImage(img)

        self.image_label.configure(image=photo)
        self.image_label.image = photo  # type: ignore


if __name__ == '__main__':
    app = Application()
    browser = ImageBrowser(app, 'preset_face_images')
    app.mainloop()
