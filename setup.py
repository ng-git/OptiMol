from setuptools import setup

# with open("README.md", 'r') as f:
#     overview_discription = f.read()

Opt = dict(name='optimol',
           version='1.0',
           description='useful module for predicting molecular conformation',
           license="MIT",
           author=["Minh", "Vivian", "Mike", "Guanning", "Weishi"],
           url="https://github.com/ShadyMikey/OptiMol",
           package=["optimol"],
           install_requires=["chemspipy", "os", "numpy", "shutil", "pandas", "scikit-learn", "pkg_resources",
                             "csv", "xgboost"],
           python_requires=">=3.0",
           package_data={'optimol': ['database_chemspider/*.txt']}
           )

if __name__ == '__main__':
    setup(**Opt,
          install_requires=["chemspipy", "numpy", "pandas", "scikit-learn", "xgboost"],
          include_package_data=True,
          package_data={'optimol': ['database_chemspider/*.txt']})
