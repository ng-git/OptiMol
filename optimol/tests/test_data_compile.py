""" Test file for data_compile.py"""

from optimol import data_compile
import pandas as pd


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
