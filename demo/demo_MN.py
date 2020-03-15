from optimol import data_compile
import pandas as pd
import os

print('testing')
id_list = data_compile.get_id()

print(id_list)
# print(os.getcwd())
user_set = data_compile.get_df_user(['user.txt'])
# print(user_set)

# this give the dataframes from database using the id
data = data_compile.get_df_database(id_list[34])
for item in data:
    print(item)

user_set = data_compile.get_df_user(['user.txt'])
print(user_set)

