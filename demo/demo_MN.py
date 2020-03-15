from optimol import data_compile
import pandas as pd
import os

print('testing')
id_list = data_compile.get_id()

# this give the dataframes from database using the id
data = data_compile.get_df_database(id_list[34])
# for item in data:
#     print(item)

# this give out a combined dataframe to be used for ML
data_set = data_compile.get_all_dataset(set1=3)
# print(data_set)

# this make the dataframe from user input
print(os.getcwd())

user_set = data_compile.get_df_user(['user.txt'])
print(user_set)

