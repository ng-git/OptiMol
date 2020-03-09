import pandas as pd
from chemspipy import ChemSpider


test = 'CH3-CH3'
cs = ChemSpider('d0xQqfSr9KAwCQDMb10uAmp46dAADGqh')
c = cs.get_compound(2157)

a = c.mol_2d

# print(c.mol_2d)
