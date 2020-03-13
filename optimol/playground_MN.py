""" to be removed at the end
TODO: remove this file"""

from optimol import data_compile
import pandas as pd
import numpy as np


id_list = data_compile.get_id()
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(id_list[35])

# print(coord_3d)
# print(coord_2d.dtypes)
del coord_2d['atom']
del coord_2d['connect_to']
del coord_2d['2d_z']


del coord_3d['atom']
del coord_3d['connect_to']

coord = pd.concat([coord_2d,coord_3d], axis=1)
print(coord)
print(coord.columns.values)

