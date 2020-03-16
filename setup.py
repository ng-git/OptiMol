from setuptools import setup

# with open("README.md", 'r') as f:
#     overview_discription = f.read()

Opt = dict(package=["optimol"],
           python_requires=">=3.0"
           )

if __name__ == '__main__':
    setup(**Opt,
          name='optimol',
          version='0.1',
          description='useful package for predicting 3D molecular conformation from 2D design',
          license="MIT",
          author=["Minh", "Vivian", "Mike", "Guanning", "Weishi"],
          url="https://github.com/ng-git/OptiMol",
          install_requires=["chemspipy", "numpy", "pandas", "scikit-learn", "xgboost", ],
          include_package_data=True,
          package_data={'database_chemspider': ['*.txt'],
                        'sample_data': ['*.txt']})
