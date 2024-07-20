# Simple flow for using FACE01

When coding a program that uses FACE01, code `initialize` and `logger` first.  
This will read the configuration file `config.ini` and log errors etc.  
Choose a section of config.ini according to your usage, or inherit DEFAULT and add a new one.  

```python
# Import Initialize class
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

# Initialize
CONFIG: Dict =  Initialize('DEFAULT').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
```

Next, we have to make `generator` for load contiguous frame datas.
```python
# Import Core class
from face01lib.Core import Core

# Make generator
gen = Core().common_process(CONFIG)
```

By using common_process method of Core class, a series of flow from face-detection to face-recognition can be performed smoothly.

For getting datas, we have to call `__next__`.
```python
while True:

    # Call __next__() from the generator object
    frame_datas_array = gen.__next__()
```

`frame_datas_array` contains various data.
Set what kind of data to get and include in config.ini.