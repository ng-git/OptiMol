""" Test file for data_compile.py"""

from optimol import data_compile
import pandas as pd
import os

path = os.path.dirname(os.path.realpath(__file__))


def test_get_all_dataset_input_combo():
    """ Check for invalid set combination"""

    id_list = data_compile.get_id()
    try:
        data_compile.get_all_dataset(1, -1)
        raise Exception()
    except ValueError:
        pass

    try:
        data_compile.get_all_dataset(len(id_list) + 1, 1)
        raise Exception()
    except ValueError:
        pass

    try:
        data_compile.get_all_dataset(1, len(id_list) + 1)
        raise Exception()
    except ValueError:
        pass


def test_get_all_dataset_input():
    """ Check for input type"""

    try:
        data_compile.get_all_dataset(1, 0.1)
        raise Exception()
    except TypeError:
        pass

    try:
        data_compile.get_all_dataset(0.1, 1)
        raise Exception()
    except TypeError:
        pass

    try:
        data_compile.get_all_dataset('text', 1)
        raise Exception()
    except TypeError:
        pass


def test_get_df_database_invalid_id():
    """ Check for invalid id"""

    try:
        data_compile.get_df_database(1)
        raise Exception()
    except ValueError:
        pass


def test_get_df_database_input():
    """ Check input type"""

    try:
        data_compile.get_df_database(0.1)
        raise Exception()
    except TypeError:
        pass


def test_trim_hydrogen_input():
    """ Check input type"""

    try:
        data_compile.trim_hydrogen(1, pd.DataFrame())
        raise Exception()
    except TypeError:
        pass

    try:
        data_compile.trim_hydrogen(pd.DataFrame(), 1)
        raise Exception()
    except TypeError:
        pass


def test_atom_connect_col():
    """ Check for existed connect_to column"""
    # dataframe already have connect_to column
    [_, test_bond] = data_compile.get_df(path + '/samples/user.txt')
    test_df = data_compile.get_df_user([path + '/samples/user.txt'])
    try:
        data_compile.atom_connect(test_df, test_bond)
        raise Exception()
    except ValueError:
        pass


def test_atom_connect_input():
    """ Check input type"""

    try:
        data_compile.atom_connect(1, 1)
        raise Exception()
    except TypeError:
        pass


def test_atom_periodic_number_convert_periodic_col():
    """ Check for existed periodic number column"""

    # dataframe already have periodic column
    test_df = data_compile.get_df_user([path+'/samples/user.txt'])
    try:
        data_compile.atom_periodic_number_convert(test_df)
        raise Exception()
    except ValueError:
        pass


def test_atom_periodic_number_convert_input_type():
    """ Check input type"""

    try:
        data_compile.atom_periodic_number_convert(1)
        raise Exception()
    except TypeError:
        pass


def test_get_df_database_input_type():
    """ Check input type"""

    try:
        data_compile.get_df_database(1.327)
        raise Exception()
    except TypeError:
        pass


def test_get_df_database_input_value():
    """ Check input value"""

    try:
        data_compile.get_df_database(1)
        raise Exception()
    except ValueError:
        pass


def test_get_df_input_type():
    """ Check dimension input value"""
    try:
        data_compile.get_df('asdf.txt', dim=10)
        raise Exception()
    except ValueError:
        pass


def test_df_cleaner_input_dimension():
    """ Check dataframe input dimension"""

    test_df = pd.DataFrame({'col_1': [1, 2],
                            'col_2': [5, 6]})
    cleaned_df = pd.DataFrame(columns=['col_1', 'col_2'])
    try:
        data_compile.df_cleaner(test_df, cleaned_df)
        raise Exception()
    except ValueError:
        pass


def test_df_cleaner_input_type():
    """ Check input type"""
    try:
        data_compile.df_cleaner(18964, 'text')
        raise Exception()
    except TypeError:
        pass
