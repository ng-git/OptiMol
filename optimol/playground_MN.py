from optimol import data_compile
import pandas as pd
import numpy as np


id_list = data_compile.get_id()
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(id_list[35])

# print(id_list[35])
# for item in [coord_2d, bond_2d]:
#     print(item)

element = dict({'C': 6, 'O': 8, 'H': 1, 'N': 7})

coord_2d['atom_#'] = None
for i in range(coord_2d.shape[0]):
    for elem in element.keys():
        if elem in coord_2d['atom'][i]:
            coord_2d['atom_#'][i] = element[elem]


atom_1 = None
atom_2 = None
coord_2d['connect'] = np.empty((len(coord_2d), 0)).tolist()

for i in range(coord_2d.shape[0]):
    atom_1 = int(bond_2d['atom_1'][i])
    atom_2 = int(bond_2d['atom_2'][i])
    for j in range(int(bond_2d['bond_type'][i])):
        coord_2d['connect'][atom_1 - 1].append(atom_2 - 1)  # subtract 1 to shift values to zero-based
        coord_2d['connect'][atom_2 - 1].append(atom_1 - 1)


print(coord_2d)



