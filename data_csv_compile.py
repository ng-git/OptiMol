import pandas as pd
import numpy as np


# get the number of atoms to cut off the text rows
atom_amount = int(pd.read_csv('aspirin_2d.txt', nrows=1).iloc[0, 0][1:3])

data_2d = pd.read_csv('aspirin_2d.txt', nrows=atom_amount)

