from setuptools import setup

with open("README", 'r') as f:
    overview_discription = f.read()

Opt = dict(name='optimol',
           version='1.0',
           description='useful module for predicting molecular conformation',
           license="MIT",
           author=["Minh", "Vivian", "Mike", "Guanning", "Weishi"],
           url="https://github.com/ShadyMikey/OptiMol",
           package=["optimol"],
           install_requires=["ChemSpider", "os", "numpy", "shutil", "pandas", "sklearn", "pkg_resources",
                             "csv", "xgboost"],
           python_requires=">=3.0",
           # setup_requires = SETUP_REQUIRES
           )

if __name__ == '__main__':
    setup(**Opt, install_requires=["ChemSpider", "os", "numpy", "shutil", "pandas", "sklearn", "pkg_resources",
                                   "csv", "xgboost"])
    


 
