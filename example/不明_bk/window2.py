import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from ttkbootstrap import Style
from watchdog.events import DirModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer


class DirectoryObserver:
    def __init__(self, path, callback):
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_modified = callback
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=False)
        self.observer.start()


# 画像ブラウザクラスの定義
class ImageBrowser:
    def __init__(self, master, path):
        self.master = master  # 親ウィジェットを保存
        self.frame = ttk.Frame(master)  # フレームを作成
        self.frame.pack(fill="both", expand=True)  # フレームをパック

        self.image_list = []  # 画像リストの初期化
        self.load_images(path)  # 画像を読み込む

        self.canvas_frame = ttk.Frame(self.frame)  # キャンバスのフレームを作成
        self.canvas_frame.pack(side="top", fill="both", expand=True)  # キャンバスのフレームをパック

        self.canvas = tk.Canvas(self.canvas_frame)  # キャンバスを作成
        self.canvas.pack(side="left", fill="both", expand=True)  # キャンバスをパック

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)  # スクロールバーを作成
        self.scrollbar.pack(side="right", fill="y")  # スクロールバーをパック

        self.canvas.configure(yscrollcommand=self.scrollbar.set)  # キャンバスにスクロールバーを設定

        # キャンバスの設定イベントにメソッドをバインド
        self.canvas.bind('<Configure>', self.on_configure)
        self.canvas_frame.bind_all(
            '<MouseWheel>', self.on_mousewheel)  # マウスホイールイベントにメソッドをバインド

        self.photos = []  # 写真リストの初期化

        self.image_label = ttk.Label(self.frame)  # 画像ラベルを作成
        self.image_label.pack(fill="both", expand=True)  # 画像ラベルをパック

        self.current_image_path = None  # 現在の画像パスをNoneに設定
        if self.image_list:  # 画像リストが空でない場合
            # 現在の画像パスをリストの最初の画像に設定
            self.current_image_path = self.image_list[0]
            self.master.after(100, self.show_image,
                              self.current_image_path)  # 画像を表示するメソッドを呼び出す

        self.observer = DirectoryObserver(path, self.load_images)


# 画像をロードするメソッド
def load_images(self, path):  # オブジェクトの場合
    if isinstance(path, DirModifiedEvent):
        path = path.src_path  # DirModifiedEventオブジェクトからパスを取得
    # pathが文字列の場合
    elif isinstance(path, str):
        path = path  # path自体がパスであるとする
    else:
        raise TypeError('Invalid type for event: {}'.format(type(path)))

    for file_name in os.listdir(path):  # ディレクトリ内のファイル名を繰り返す
        if file_name.endswith(('.png', '.jpg', '.jpeg')):  # ファイルが画像の場合
            self.image_list.append(os.path.join(path, file_name))  # 画像リストに追加

    # キャンバス設定イベントのハンドラ
    def on_configure(self, event):
        self.canvas.delete('all')  # キャンバス上の全てのアイテムを削除
        self.photos = []  # 写真リストをリセット
        x = 10
        y = 10
        thumbnail_width = 100
        thumbnail_height = 100
        for image_path in self.image_list:  # 画像リストを繰り返す
            img = Image.open(image_path)  # 画像を開く
            img.thumbnail((thumbnail_width, thumbnail_height))  # サムネイルサイズに変更
            photo = ImageTk.PhotoImage(img)  # PhotoImageに変換
            self.photos.append(photo)  # 写真リストに追加

            image_id = self.canvas.create_image(x, y, image=photo, anchor='nw')  # キャンバスに画像を描画
            self.canvas.tag_bind(image_id, '<Double-Button-1>', lambda e, path=image_path: self.show_image(path))  # ダブルクリックイベントにメソッドをバインド

            x += thumbnail_width + 10  # 次の画像のx座標を計算
            if x > event.width - thumbnail_width:  # 画像がキャンバスの幅を越える場合
                x = 10  # x座標をリセット
                y += thumbnail_height + 10  # y座標を増加

        self.canvas.configure(scrollregion=self.canvas.bbox('all'))  # スクロール領域を全てのアイテムが含まれるように設定

        if self.current_image_path:  # 現在の画像パスが設定されている場合
            self.show_image(self.current_image_path)  # 画像を表示

    # マウスホイールイベントのハンドラ
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  # キャンバスをスクロール

    # 画像を表示するメソッド
    def show_image(self, image_path):
        self.current_image_path = image_path  # 現在の画像パスを更新
        img = Image.open(image_path)  # 画像を開く
        img.thumbnail((self.master.winfo_width(), max(1, self.master.winfo_height() // 2)))  # サムネイルサイズに変更
        photo = ImageTk.PhotoImage(img)  # PhotoImageに変換

        self.image_label.configure(image=photo)  # 画像ラベルに画像を設定
        self.image_label.image = photo  # 画像ラベルに画像を保存


if __name__ == '__main__':
    # メインウィンドウを作成
    root = tk.Tk()
    root.geometry("1000x1000")  # ウィンドウの幅と高さを設定

    # メニューバーを作成
    menubar = tk.Frame(root)
    menubar.pack(side="top", fill="x")

    # アイコンを読み込む
    icon = tk.PhotoImage(file="assets/images/Logo_dist.png")

    # メニューアイテムを作成
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)

    # メニューボタンを作成
    menu_button = tk.Menubutton(menubar, text="File", image=icon, compound="left", menu=file_menu)
    menu_button.pack(side="left")

    # "Run"ボタンを作成
    run_button = tk.Button(menubar, text="実行")
    run_button.pack(side="right")

    # エリアを保持するフレームを作成
    frame_holder = tk.Frame(root)
    frame_holder.pack(expand=True, fill="both")

    # 2x2のグリッドのフレームを作成
    n = 2
    frames = []
    for i in range(n):
        row = []
        for j in range(n):
            frame = tk.Frame(frame_holder, bd=2, relief="groove")
            frame.grid(row=i, column=j, sticky="nsew")
            tk.Label(frame, text=f"Area {n*i + j + 1}").pack()  # エリアの番号を表示するラベルを作成
            row.append(frame)
        frames.append(row)

    # グリッドのウェイトを設定
    for i in range(n):
        frame_holder.grid_rowconfigure(i, weight=1)
        frame_holder.grid_columnconfigure(i, weight=1)

    # Area 2にImageBrowserを作成
    browser = ImageBrowser(frames[0][1], 'output')
    # browser = ImageBrowser(frames[0][1], 'preset_face_images')

    def on_closing():
        browser.observer.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()  # メインループを開始
