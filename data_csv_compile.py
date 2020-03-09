import pandas as pd
import numpy as np


# get the number of atoms to in 2D cut off the text rows
atom_amount = int(pd.read_csv('aspirin_2d.txt', skiprows=1).iloc[0, 0][1:3])
print(atom_amount)
# get the dataframe for 2d coord
coord_2d = pd.read_csv('aspirin_2d.txt', skiprows=2, nrows=atom_amount)
# get the bonding for 2d coord
bond_2d = pd.read_csv('aspirin_2d.txt', skiprows=3+atom_amount, nrows=atom_amount)


# get the number of atoms in 3D to cut off the text rows
atom_amount = int(pd.read_csv('aspirin_3d.txt', skiprows=1).iloc[0, 0][1:3])
print(atom_amount)
# get the dataframe for 2d coord
coord_3d = pd.read_csv('aspirin_3d.txt', skiprows=2, nrows=atom_amount)
# get the bonding for 2d coord
bond_3d = pd.read_csv('aspirin_3d.txt', skiprows=3+atom_amount, nrows=atom_amount)

