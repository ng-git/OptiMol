from optimol import data_compile
import pandas as pd
import numpy as np


id_list = data_compile.get_id()
# [coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(id_list[35], raw=True, hydrogen=True)
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(id_list[35], raw=False, hydrogen=False)

# print(id_list[35])
# for item in [coord_2d, coord_3d]:
#     print(item)

# print(coord_2d)

# coord_2d = data_compile.atom_periodic_number_convert(coord_2d)
# coord_2d = data_compile.atom_connect(coord_2d, bond_2d)
# coord_3d = data_compile.atom_periodic_number_convert(coord_3d)
# coord_3d = data_compile.trim_hydrogen(coord_3d)
# coord_3d = coord_3d[coord_3d['periodic_#'] != 1]
# size = coord_3d.count()[0]
print(coord_3d)
print(bond_3d)


