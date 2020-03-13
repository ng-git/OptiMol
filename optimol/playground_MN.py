""" to be removed at the end
TODO: remove this file"""

from optimol import data_compile
import pandas as pd
import numpy as np


id_list = data_compile.get_id()
# print(id_list[223])
# all = data_compile.get_all_dataset()
# print(all)

# bug_case = id_list[255]
# bug_case = id_list[1]

filename = './database_chemspider/' + str(bug_case) + '_3d.txt'
print(bug_case)
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(bug_case)

print(coord_2d)
