# What to do when dlib.DLIB_USE_CUDA is False
FACE01 uses CUDA to maximize GPU utilization. Normally, by typing `pip install dlib` in the terminal, CUDA can be used according to the usage environment.
To check if CUDA is available:
```bash
(FACE01)
FACE01 $ pip freeze | grep dlib
dlib==19.24.0
(FACE01)
FACE01 $ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
True
>>>
```
If `False` at this time, CUDA cannot be used.
## Uninstall Dlib
Please uninstall Dlib once as follows.
```bash
pip uninstall dlib
```
## Extract `dlib-19.24.tar.bz2`
Unzip `dlib-19.24.tar.bz2` to create `dlib-19.24` directory.
```bash
tar xvjf dlib-19.24.tar.bz2
cd dlib-19.24
```
## Build with `gcc-8`
The gcc version is very important when building Dlib. `gcc` versions later than `8` are ***not*** supported. Specify gcc-8 etc. as follows.
```bash
(FACE01)
FACE01/dlib-19.24 $ export CC=/usr/bin/gcc-8
(FACE01)
FACE01/dlib-19.24 $ export CXX=/usr/bin/g++-8
(FACE01)
FACE01/dlib-19.24 $ python setup.py install
```
## Check if installed
```bash
(FACE01)
FACE01/dlib-19.24 $ pip freeze | grep dlib
dlib==19.24.0
(FACE01)
FACE01/dlib-19.24 $ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
True
>>>
(FACE01)
FACE01/dlib-19.24 $
```
If you can confirm that it is `True`, you are finished:tada:.