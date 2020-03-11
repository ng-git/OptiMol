""" This module contain functions to retrieve and process data from the database folder"""

import os
import numpy as np
import shutil
import csv
import pandas as pd

ROOT = os.getcwd()
DATABASE = ROOT + '/database_chemspider'


def get_df_database(id_num):
    """ Access the database folder using the id number to get a list of dataframes contain 2D and 3D data
        :param id_num: id number of the molecule
        :type id_num: int, str

        :return coord_2d: atom 2D coordinates
        :return bond_2d: atom 2D bonding types and arrangement
        :return coord_3d: atom 3D coordinates
        :return bond_3d: atom 3D bonding types and arrangement
        :rtype coord_2d, bond_2d, coord_3d, bond_3d: pandas.DataFrame"""

    # check input type
    if not isinstance(id_num, (int, str)):
        raise TypeError()

    # in case id is string type
    if isinstance(id_num, str):
        # check for numeric input
        if not id_num.isdigit():
            raise ValueError('Invalid ID number')
        else:
            # cast to int if numeric
            id_num = int(id_num)

    # check valid id
    if id_num not in get_id():
        raise ValueError()

    # access database
    os.chdir(DATABASE)

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
        raise ValueError('Invalid dimension!')

    # get the number of atoms to cut off the text rows
    check = False
    i = 0
    atom = None
    bond_amount = None
    # go through each row
    while check is False:
        values = pd.read_csv(filename).iloc[i, 0].split()
        i = i + 1
        # check the first value to be int, which is number of atoms
        if values[0].isdigit():
            atom = int(values[0])
            bond_amount = int(values[1])
            check = True

    # crop the dataframe according to number of atoms
    raw_coord = pd.read_csv(filename, skiprows=i+1, nrows=atom)

    # adjust crop point according to dimension type due to data format
    if dim is 2:
        i = i + 1

    # crop the dataframe of bonding
    raw_bond = pd.read_csv(filename, skiprows=atom + i + 1, nrows=bond_amount)

    # prepare returning dataframes to fit with input dimension
    bond = pd.DataFrame(columns=['atom_1', 'atom_2', 'bond_type'])
    coord = pd.DataFrame(columns=[str(dim) + 'd_x', str(dim) + 'd_y', str(dim) + 'd_z', 'atom'])

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
    if False in [isinstance(df, pd.DataFrame),
                 isinstance(new_df, pd.DataFrame)]:
        raise TypeError()

    if df.shape[1] is not 1:
        raise ValueError('Input dataframe should be a column')

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


def sample_subset(directory=DATABASE, size=50):
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

    from chemspipy import ChemSpider

    # compile id list for calling molecules
    id_list = get_id()

    directory = DATABASE
    # make directory database_chemspider/ if needed
    if os.path.isdir(directory):
        print('Database folder already existed! Aborting... \n Please remove the folder and rerun')
        exit()
    else:
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
