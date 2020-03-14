""" to be removed at the end
TODO: remove this file"""

from optimol import data_compile
import pandas as pd
import numpy as np


id_list = data_compile.get_id()
# print(id_list[223])
# [train, test] = data_compile.get_all_dataset(set1=10, set2=5)
# print([train, test])

# user = data_compile.get_df('./sample_data/user.txt')
# input_list = ['./sample_data/less_than_4.txt']
# input_list = ['./sample_data/empty.txt']
input_list = ['./sample_data/user.txt']
user = data_compile.get_df_user(input_list)
user1 = data_compile.atom_periodic_number_convert(user)
print(user)
print(user.columns)