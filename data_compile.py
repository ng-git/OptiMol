""" This module contain functions to retrieve and process data from the database folder"""

import os
import numpy as np
import shutil
import csv
import pandas as pd
from chemspipy import ChemSpider

ROOT = os.getcwd()


def df_cleaner(df, new_df):
    """ Reformat input dataframe to be more usable
        :param df: input dataframe from reading id.txt file, only has 1 column of white space separated values
        :type df: pandas.DataFrame

        :param new_df: output dataframe
        :type new_df: pandas.DataFrame"""

    # check input types
    if False in [isinstance(df, type(pd.DataFrame)),
                 isinstance(new_df, type(pd.DataFrame))]:
        raise TypeError()

    # go through each row
    for index in range(df.shape[0]):
        line = df.iloc[index, 0]
        # separate values between white spaces
        x = line.split()
        new_df.loc[index] = x[0:new_df.shape[1]]

    return new_df


def sample_dir(directory, size=50):
    """ Create a smaller database folder inside the main database folder for testing
        :param directory: directory of the database from root
        :param size: the size of the folder

        :type directory: str
        :type size: int

        :return a list of sample id in the created folder
        :rtype id_results: list"""

    # check for invalid input
    if not os.path.exists(directory):
        raise Exception('Directory does not exist!')

    # access data directory
    os.chdir(directory)
    output_dir = './sample' + str(size)
    # make 100 samples folder to run smaller test first
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        text = input("Folder already exist, clear folder and resampling? \
            \n Press \"y\" to continue, or any keys to abort. \n ")
        if 'y' is text:
            shutil.rmtree(output_dir)
            os.mkdir(output_dir)
        else:
            exit()

    id_list = get_id()
    # get index of 100 random value
    index = np.random.randint(0, high=len(id_list), size=size)

    # copy all items to subdir.
    id_results = []
    for i in index:
        try:
            shutil.copy2(str(id_list[i]) + '_2d.txt', output_dir)
            shutil.copy2(str(id_list[i]) + '_3d.txt', output_dir)
            id_results.append(id_list[i])
            print(str(id_list[i]) + ' done')
        except shutil.SameFileError:
            print(str(id_list[i]) + ' already done in the past')

    os.chdir('../')
    return id_results


def get_id():
    """ Return a list of id of the whole database
        :rtype id_results: list"""

    results = []
    # always open csv file in root dir
    with open(ROOT + "/id.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')  # change contents to floats
        for row in reader:  # each row is a list
            results.append(row)

    # remove non id value
    id_result = []
    for i in range(1, len(results)):
        id_result.append(int(results[i][0]))

    # check for duplicate and remove them
    if len(id_result) != len(set(id_result)):
        id_result = list(set(id_result))

    return id_result


def database_setup():
    """ Download 2D and 3D molecule structure from ChemSpider sever to create a database"""

    # compile id list for calling molecules
    id_list = get_id()

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
