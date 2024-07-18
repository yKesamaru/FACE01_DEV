# Step-by-step to use FACE01 library
**Welcome to FACE01 world!**

In this article, I will introduce the necessary knowledge and techniques to create an application that uses face recognition using FACE01 with an example program.

Are you ready?

Let's check the **checks you must pass** as step. 1.

TOC
1. [Step-by-step to use FACE01 library](#step-by-step-to-use-face01-library)
   1. [Checks you must pass](#checks-you-must-pass)
   2. [Register face images](#register-face-images)
   3. [activate virtual python mode](#activate-virtual-python-mode)
   4. [Check vim installed](#check-vim-installed)
2. [Simple flow for using FACE01](#simple-flow-for-using-face01)
3. [Simple face recognition](#simple-face-recognition)
4. [Display GUI window](#display-gui-window)
5. [Display 'telop' and 'logo' images which you're company's.](#display-telop-and-logo-images-which-youre-companys)
6. [Want to benchmark?](#want-to-benchmark)
7. [Example list](#example-list)
8. [Troubleshooting:thinking:](#troubleshootingthinking)
   1. [CUDA not working](#cuda-not-working)
   2. [What to do when dlib.DLIB\_USE\_CUDA is False](#what-to-do-when-dlibdlib_use_cuda-is-false)

## Checks you must pass
✅
- [x] Basic operation of Python
- [x] Basic operation of Docker
- [x] Basic operation of Linux terminal
- [x] (If using Nvidia GPU) CUDA driver is already installed


Have you checked everything?  
OK! Let's get started!


## [Register face images](register_faces.md)
This article describes how to register face images.

See [here](register_faces.md).


## activate virtual python mode
Start the virtual environment using venv of the Python standard library.

```bash
# activate venv
. bin/activate
```


## Check vim installed
The Docker Image comes with vim installed so you can edit `conf.ini`.

```bash
# Check vim installed
which vim
```


# [Simple flow for using FACE01](simple_flow.md)
It is an example of how to use FACE01, but let's look at a simple flow.

See [here](simple_flow.md).



# [Simple face recognition](simple.md)
Let' try `simple.py`.
simple.py is an example script for CUI behavior.

```python
python example/simple.py
```
See [here](simple.md).


# [Display GUI window](display_GUI_win.md)
Want to display in a cool GUI window?  
Try `example/display_GUI_window.py`.  
See [here](display_GUI_win.md).

```python
python example/display_GUI_window.py
```
See [here](simple.md).


# [Display 'telop' and 'logo' images which you're company's.](ch_telop.md)
Do you want your window to display your company logo or something?  
Of course you can!  
See [here](ch_telop.md).


# [Want to benchmark?](benchmark_CUI.md)
See [here](benchmark_CUI.md).

# Example list
```python
# 1. Simple
python example/simple.py

# 2. Display GUI window
python example/display_GUI_window.py

# 3. logging
python example/example_logging.py

# 4. data structure
python example/data_structure.py

# 5. Benchmark with CUI mode
python example/benchmark_CUI.py

# 6. Benchmark with GUI mode
python example/benchmark_GUI_window.py

# Other
- example/aligned_crop_face.py
- example/anti_spoof.py
- example/distort_barrel.py
- example/draw_datas.py
- example/face_coordinates.py
- example/get_encoded_data.py
- example/lightweight_GUI.py
...and others.
```

**For more information about FACE01 many Classes and methods, see [FACE01 document](https://ykesamaru.github.io/FACE01_SAMPLE/).**

# Troubleshooting:thinking:
## CUDA not working
See [Remove all cuda lib and re-install method](reinstall_gpu.md)
## What to do when dlib.DLIB_USE_CUDA is False
See [What to do when dlib.DLIB_USE_CUDA is False](dlib.DLIB_USE_CUDA.md)