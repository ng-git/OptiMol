import pandas as pd
import numpy as np


# get the number of atoms to in 2D cut off the text rows
atom_2d = int(pd.read_csv('aspirin_2d.txt', skiprows=1).iloc[0, 0][1:3])
print(atom_2d)
# get the dataframe for 2d coord
coord_2d = pd.read_csv('aspirin_2d.txt', skiprows=2, nrows=atom_2d)
# get the bonding for 2d coord
bond_2d = pd.read_csv('aspirin_2d.txt', skiprows=3+atom_2d, nrows=atom_2d)


# get the number of atoms in 3D to cut off the text rows
atom_3d = int(pd.read_csv('aspirin_3d.txt', skiprows=1).iloc[0, 0][1:3])
print(atom_3d)
# get the dataframe for 2d coord
coord_3d = pd.read_csv('aspirin_3d.txt', skiprows=2, nrows=atom_3d)
# get the bonding for 2d coord
bond_3d = pd.read_csv('aspirin_3d.txt', skiprows=3+atom_3d, nrows=atom_3d)


def df_cleaner(df, new_df):
    for index in range(df.shape[0]):
        line = df.iloc[index, 0]
        x = line.split()
        new_df.loc[index] = x[0:new_df.shape[1]]
    return new_df


coord_2d_fixed = pd.DataFrame(columns=['2d_x', '2d_y', '2d_z', 'atom'])
coord_2d_fixed = df_cleaner(coord_2d, coord_2d_fixed)

coord_3d_fixed = pd.DataFrame(columns=['3d_x', '3d_y', '3d_z', 'atom'])
coord_3d_fixed = df_cleaner(coord_3d, coord_3d_fixed)

bond_2d_fixed = pd.DataFrame(columns=['atom_1', 'atom_2', 'bond_type'])
bond_2d_fixed = df_cleaner(bond_2d, bond_2d_fixed)

bond_3d_fixed = pd.DataFrame(columns=['atom_1', 'atom_2', 'bond_type'])
bond_3d_fixed = df_cleaner(bond_3d, bond_3d_fixed)



