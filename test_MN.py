import os
import data_compile
import pandas as pd


id_list = data_compile.get_id()


index = id_list[50]
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(index)
print(coord_2d)
print(bond_2d)
print(coord_3d)
print(bond_3d)
