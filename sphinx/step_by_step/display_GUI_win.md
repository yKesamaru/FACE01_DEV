# GUIウィンドウを作成する

GUIウィンドウを描画するシンプルなエグザンプルです。
`python example/display_GUI_window.py`.

<br />
<div style="display: flex; align-items: center; justify-content: flex-end;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative; margin-right: 10px;">
        <p style="margin: 10;">複数人の顔認証もラクラクです⭐️''</p>
        <p style="margin: 10;">処理が遅い場合はconfig.iniの設定を変更しましょう。i/oが遅い場合、処理速度に影響することがあります。そんなときはcrop_face_imageをfalseにするかfrequency_crop_imageの値を上げましょう。</p>
        <div style="position: absolute; top: 50%; right: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 15px solid white; transform: translateY(-50%);"></div>
    </div>
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00129-2005948764.png" alt="説明文" width="200" style="border-radius: 50%; object-fit: cover;">
</div>
<br />

## Result
```bash
...
麻生太郎
         similarity      99.1%
         coordinate      (114, 528, 276, 366)
         time    2022,07,20,07,14,56,229442
         output  output/麻生太郎_2022,07,20,07,14,56,254172_0.39.png
 -------

菅義偉
         similarity      99.3%
         coordinate      (124, 199, 283, 40)
         time    2022,07,20,07,14,56,229442
         output  output/麻生太郎_2022,07,20,07,14,56,254172_0.39.png
 -------

...

```
![FACE01_GUI](https://user-images.githubusercontent.com/93259837/180339656-7ef7baea-480f-4d78-b29b-e8e12bc85189.gif)


