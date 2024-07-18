# If you want to get only face recognition

```bash
# activate virtual environment
source bin/activate

# run script
python example/simple.py
```

## Result
```bash

[2022-09-27 19:20:48,174] [face01lib.load_priset_image] [simple.py] [INFO] Loading npKnown.npz
菅義偉 
         similarity              99.1% 
         coordinate              (138, 240, 275, 104) 
         time                    2022,09,27,19,20,49,835926 
         output                   
 -------

麻生太郎 
         similarity              99.6% 
         coordinate              (125, 558, 261, 422) 
         time                    2022,09,27,19,20,49,835926 
         output                   
 -------
 ...
```

The face images are output to the `/output/` folder.

![](https://raw.githubusercontent.com/yKesamaru/FACE01_SAMPLE/master/img/PASTE_IMAGE_2022-07-20-07-36-26.png)

