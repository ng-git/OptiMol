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
