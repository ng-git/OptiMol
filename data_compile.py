""" This module contain functions to retrieve and process data from the database folder"""

import os
import numpy as np
import shutil
import csv
import pandas as pd
from chemspipy import ChemSpider

ROOT = os.getcwd()


def get_df_database(id_num):
    """ Access the database folder using the id number to get a list of dataframes contain 2D and 3D data
        :param id_num: id number of the molecule
        :type id_num: int

        :return coord_2d: atom 2D coordinates
        :return bond_2d: atom 2D bonding types and arrangement
        :return coord_3d: atom 3D coordinates
        :return bond_3d: atom 3D bonding types and arrangement
        :rtype coord_2d, bond_2d, coord_3d, bond_3d: pandas.DataFrame"""

    # check input type
    if not isinstance(id_num, int):
        raise TypeError()

    # check valid id
    id_list = get_id()
    if id_num not in id_list:
        raise ValueError()

    os.chdir(ROOT + '/database_chemspider')

    # get dataframe of 2d coord and bonding
    filename_2d = str(id_num) + '_2d.txt'
    [coord_2d, bond_2d] = get_df(filename_2d, dim=2)

    # get dataframe of 3d coord and bonding
    filename_3d = str(id_num) + '_3d.txt'
    [coord_3d, bond_3d] = get_df(filename_3d, dim=3)

    os.chdir(ROOT)

    return [coord_2d, bond_2d, coord_3d, bond_3d]


def get_df(filename, dim=2):
    """ Extract the atom coordinates and bonding data from txt file according to provided dimension
        Can be used for both database and user input file
        :param filename: text file name
        :param dim: dimension of the molecule structure in the text file
        :type filename: str
        :type dim int

        :return coord, bond: coordinate and bonding data from the text file
        :rtype coord, bond: pandas.DataFrame"""

    # check input type
    if False in [isinstance(filename, str),
                 filename.endswith('.txt'),
                 isinstance(dim, int)]:
        raise TypeError()

    # check dimension input value
    if dim not in [2, 3]:
        raise ValueError()

    # get the number of atoms to cut off the text rows
    atom = int(pd.read_csv(filename, skiprows=1).iloc[0, 0][1:3])
    # get the dataframe for coord
    raw_coord = pd.read_csv(filename, skiprows=2, nrows=atom)
    # get the bonding
    raw_bond = pd.read_csv(filename, skiprows=3 + atom, nrows=atom)

    # prepare returning dataframes to fit with input dimension
    bond = pd.DataFrame(columns=['atom_1', 'atom_2', 'bond_type'])
    if dim == 2:
        coord = pd.DataFrame(columns=['2d_x', '2d_y', '2d_z', 'atom'])
    else:
        coord = pd.DataFrame(columns=['3d_x', '3d_y', '3d_z', 'atom'])

    # fix dataframe format
    coord = df_cleaner(raw_coord, coord)
    bond = df_cleaner(raw_bond, bond)

    return [coord, bond]


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


def sample_subset(directory, size=50):
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