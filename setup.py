from setuptools import setup

with open("README", 'r') as f:
    overview_discription = f.read()

Opt = dict(name = 'OptMol',
           version = '1.0',
           description = 'useful module for predicting molecular conformation',
           license = "MIT",
           author = "Minh", "Vivian","Mike","Guanning","Weishi",
           url = "https://github.com/ShadyMikey/OptiMol",
           package = "ChemSpider","os","numpy","shutil","pandas",
           install_requires = REQUIRES
           python_requires = PYTHON_REQUIRES
           setup_requires = SETUP_REQUIRES)

if __name__ == '__main__':
    setup(**Opt)
    


 
