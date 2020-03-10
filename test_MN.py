import os
import data_compile
import pandas as pd


id_list = data_compile.get_id()
# id_list = data_compile.sample_dir('./database_chemspider', size=50)


# get the number of atoms to in 2D cut off the text rows
# atom_2d = int(pd.read_csv('aspirin_2d.txt', skiprows=1).iloc[0, 0][1:3])
# directory = './database_chemspider/' + str(id_list[13]) + '_2d.txt'
#
# test = pd.read_csv(directory, skiprows=1).iloc[0, 0][1:3]
# atom_2d = int(pd.read_csv(directory, skiprows=1).iloc[0, 0][1:3])


# print(atom_2d)
# get the dataframe for 2d coord
# raw_coord_2d = pd.read_csv(directory, skiprows=2, nrows=atom_2d)
# # get the bonding for 2d coord
# raw_bond_2d = pd.read_csv(directory, skiprows=3+atom_2d, nrows=atom_2d)
#
# coord_2d = pd.DataFrame(columns=['2d_x', '2d_y', '2d_z', 'atom'])
#
# coord_2d = data_compile.df_cleaner(raw_coord_2d, coord_2d)
#
# print(coord_2d)


# index = id_list[3]
# [coord_test, bond_test] = data_compile.get_df('./database_chemspider/' +
#                                               str(index) + '_2d.txt', dim=2)
# print(index)
# print(coord_test)
# print(bond_test)
#
# index = id_list[3]
# [coord_test, bond_test] = data_compile.get_df('./database_chemspider/' +
#                                               str(index) + '_3d.txt', dim=3)
# print(index)
# print(coord_test)
# print(bond_test)
#
# index = id_list[50]
# [coord_test, bond_test] = data_compile.get_df('./database_chemspider/' +
#                                               str(index) + '_2d.txt', dim=2)
# print(index)
# print(coord_test)
# print(bond_test)
#
# index = id_list[50]
# [coord_test, bond_test] = data_compile.get_df('./database_chemspider/' +
#                                               str(index) + '_3d.txt', dim=3)
# print(index)
# print(coord_test)
# print(bond_test)

index = id_list[50]
[coord_2d, bond_2d, coord_3d, bond_3d] = data_compile.get_df_database(index)
print(coord_2d)
print(bond_2d)
print(coord_3d)
print(bond_3d)
