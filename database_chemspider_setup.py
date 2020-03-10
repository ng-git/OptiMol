import os
from chemspipy import ChemSpider
import pandas as pd
import csv
import numpy as np


# compile id list for calling molecules
results = []
with open("id.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')  # change contents to floats
    for row in reader:  # each row is a list
        results.append(row)

id_list = []
for i in range(1, len(results)):
    id_list.append(int(results[i][0]))


directory = './database_chemspider/'
# make directory database_chemspider/ if needed
if not os.path.isdir(directory):
    os.mkdir(directory)

print('downloading..')
os.chdir(directory)  # change dir to database_chemspider/

# access API key
cs = ChemSpider('d0xQqfSr9KAwCQDMb10uAmp46dAADGqh')

# go through each id
for id_chemspider in id_list:
    if os.path.exists(str(id_chemspider) + '_2d.txt'):
        # pass if id already exist
        print('ID ' + str(id_chemspider) + ' already existed')
        continue

    # access molecule data
    c = cs.get_compound(id_chemspider)
    # write 2d coord and bond data
    f = open(str(id_chemspider) + '_2d.txt', 'w')
    f.write(c.mol_2d)
    f.close()

    # write 3d coord and bond data
    f = open(str(id_chemspider) + '_3d.txt', 'w')
    f.write(c.mol_3d)
    f.close()

os.chdir('../')

# file1 = open('COD-selection.txt')
# Lines = file1.readlines()
#
# print('downloading..')
# os.chdir(directory) # change dir to database_COD/
# count = 0
# for line in Lines[0:3000]:
#     # extract url and filename from each line
#     url = line[:-1]
#     filename = url[35:]
#     if os.path.exists(filename) is False:
#         import requests
#         req = requests.get(url)
#         assert req.status_code == 200 # if the download failed, this line will generate an error
#         with open(filename, 'wb') as f:
#             f.write(req.content)
#         count = count + 1
#         if count in [10000, 20000, 30000, 40000]:
#             print(str(count) + ' downloaded..')
#
# os.chdir('../') # change dir back to default
# print(str(count) + ' CIF files downloaded')