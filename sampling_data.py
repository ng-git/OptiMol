"""Copy 100 random cif samples into a folder"""

import os
import numpy as np
import shutil


# access data directory
os.chdir('./database')

# make 100 samples folder to run smaller test first
if not os.path.isdir('./sample100'):
    os.mkdir('./sample100')
else:
    text = input("Folder already exist, clear folder and resampling? \
        \n Press \"y\" to continue, or any keys to abort. \n ")
    if 'y' is text:
        shutil.rmtree('./sample100')
    else:
        exit()

# get index of 100 random value
index = np.random.randint(0, high=2999, size=100)
all_items = os.listdir('./')

# copy all 100 items to subdir.
for i in index:
    try:
        shutil.copy2(all_items[i], './sample100')
        print(all_items[i] + ' done')
    except shutil.SameFileError:
        print(all_items[i] + ' already done in the past')

os.chdir('../')
