from optimol import data_compile
import pandas as pd


id_list = data_compile.get_id()
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(id_list[35])

print(id_list[35])
for item in [coord_2d, bond_2d, coord_3d, bond_3d]:
    print(item)
