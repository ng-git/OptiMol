# OptiMol

[![Build Status](https://travis-ci.org/ng-git/OptiMol.svg?branch=master)](https://travis-ci.org/github/ng-git/OptiMol)

OptiMol is a package for predicting molecular conformations of organic compounds, currently limited to 4 most common elements, C, H, N, O.  There are four major components in this package: a data scrapping module, a data cleaning module, a machine learning module and  a visualization module.

## Table of Contents


- [Organization of the  project](#Organization-of-the-project)
- [Software Dependencies](#Software-Dependencies)
- [Project Data](#Project-Data)
- [Documentation](#Documentation)
- [Testing](#Testing)
- [Installation](#Installation)
- [Licensing](#Licensing)
- [Tutorial / Demo](#Tutorial / Demo)
- [Git Configuration](#Git-Configuration)


## Organization of the  project

The project has the following structure:

    OptiMol/
      |- optimol/
      	|- __init__.py
      	|- data_compile.py
        |- tests/
        	|- __init__.py
            |- test_data_compile.py
      |- doc/
        |- component_specifications.ipynb
        |- functional_specifications.ipynb
        |- technology review.pdf
      |- demo/
        |- demo.ipynb
      |- README.md
      |- requirements.txt
      |- setup.py
      |- setuptool.py
      |- OptiMol.yml
      |- travis.yml
      |- LICENSE
      

In the following sections we will examine these elements one by one. First, let's consider the core of the project. This is the code inside of `optimol/data_compile.py`. This file provides function that converts scrapped data (e.g. .mol or .txt ) into feedable data frames for the machine learning model.

XGBoost is the package we used to train the machine learning module. (need more stuff)

## Software Dependencies

- Python3
- For python packages see `requirements.txt` or use `OptiMol.yml` to create an environment for this package

## Project Data

In this case, the project data is rather small, and recorded in txt files.  Thus, it can be stored alongside the module code.  This is the link of data we used to train the machine learning model. (data source: http://www.chemspider.com/)  

Data: https://drive.google.com/open?id=17vfuY6pkMiZzqaDvUiW3Zl7S7d0hAw22

In this database, there are two structure files for each molecule, recording information of their 2d and 3d structure respectively. We strongly recommend name them in the form of `chemID_2d.txt` and `chemID_3d.txt` respectively to be better processed by this module.

## Documentation

`optimol/data_compile.py`

This module contain functions to retrieve and process data from the database folder. Below shows how to use this module. 

```
from optimol import * 				# import module
data_compile.get_df_database(18) 	# loading file according their chemID, 18 here
```

The outputs of this are 4 pandas data frames: 2d atom information, 2d bond information, 3d atom information and 3d bond information in order. Let look at the output of 3d bond information:

```
data_compile.get_df_database(18)[2]
```

Output:

![](https://github.com/ShadyMikey/OptiMol/blob/master/Presentation%20and%20image/image-20200313153002994.png)

The columns `3d_x`, `3d_y` and `3d_z` are the x, y ,z coordinates of atoms

`atom` stands for the atom type, while `periodic_#` stands for their periodic numbers

`connect_to` stands for what other atoms -- labelled in row numbers and as always in python the first row is labelled as 0 -- the current atom is connected to, and -1 stands for any connection to Hydrogen

`bond_1`, `bond_2` and `bond_3` stands for the numbers of single, double and triple bonds that the atom has respectively.

Atoms information of 2D molecules can be interpreted similarly as above.

## Testing

`optimol/tests` is where the local tests and sample data stored. We have built tests in `test_data_compile.py` for each function included in the software. We recommend runnning local tests byy ['nosetests'](nose.readthedocs.io/en/latest/).  The `nosetests` application traverses the directory tree in which it is issued, looking for functions with names that match the pattern `test_*`. Typically each function in the module would have a corresponding test (e.g. `test_get_df_user_edge_cases`). Typing `nosetests test_data_compile.py` into the command window will start the unit test on your computer. `travis.yml'`is also pakced for ['continuous integration'](https://docs.travis-ci.com/user/customizing-the-build). Automated code testing creates an virtual environment for software testing each time when updating the this remote repository.

## Installation

For installation and distribution we will use the python standard library `distutils` module. This module uses a `setup.py` file to install OptiMol on a particular system and set up the [PyPI page](https://pypi.python.org/pypi/optimol) for the software. This also makes it possible to install software with using `pip` and`conda`, which are package managers for Python software. The `setup.py` file reads this information from there and passes it to the `setup` function which takes care of the rest.

## Licensing

We use the MIT license to maintains copyright to the authors.

## Tutorial / Demo

A detailed tutorial and example of how to use this module is stored in `demo` as [jupyter notebook](https://jupyter.org/).

## Git Configuration

Currently there are two files in the repository which help working
with this repository, and which you could extend further:

- `.gitignore` -- specifies intentionally untracked files (such as
  compiled `*.pyc` files), which should not typically be committed to
  git (see `man gitignore`)
- `.mailmap` -- if any of the contributors used multiple names/email
  addresses or his git commit identity is just an alias, you could
  specify the ultimate name/email(s) for each contributor, so such
  commands as `git shortlog -sn` could take them into account (see
  `git shortlog --help`)
