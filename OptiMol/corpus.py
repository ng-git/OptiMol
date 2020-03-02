# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:35:49 2020

@author: Mike Huang
"""
from ccdc.io import MoleculeReader
import pandas as pd
import re
from gemmi import cif
import numpy as np

def ex_atom(file, decimal = 3):
    """
    This function is to extra atom info in a CIF file.
    file is to input the path of your target CIF file
    decimal is the decimal place for the coordinate number
    """
    # Loading file to packages
    mol_1 = MoleculeReader(file)
    doc_1 = cif.read_file(file)
    
    # find out how many atoms are there in a molelcue, which is super important
    # because the CIF file can only report a portion of atoms and generate the whole molecule based on symmetry
    s = (str(mol_1[0].formula)).split()
    atom_sum = 0
    for i in s:
        matches = re.findall('\d+', i)
        atom_sum += int(matches[0])                     # how many atoms in molecule
    
    #because of "0.XXXX" is the length of the coordinate of atoms,we need to extend the length by two to cover "0."
    decimal = decimal +2
    
    # adding Chem_ID and atoms to dataframe
    List = []
    for f in mol_1[0].atoms:
        s = str(f)
        s = s[s.find("(")+1:s.find(")")]
        List.append(s)
    data_frame = pd.DataFrame(data = List, columns = ['atoms']) # adding atom
    data_frame['Chem_ID'] = file                                # adding Chem_ID
    data_frame = data_frame[['Chem_ID','atoms']]                # rearrange the dataframe
    
    # adding atom number to dataframe
    List =[]
    for f in data_frame['atoms']:
        temp = re.findall(r'\d+', str(f))
        temp_str = int(str(temp[0]))
        List.append(temp_str)
    data_frame['atom#'] = List
    
    # adding 3D coordinate
    block = doc_1.sole_block()      # pass the value to block
    
    # X
    col_x = block.find_values('_atom_site_fract_x')
    List = []
    List_multi = []
    for n, x in enumerate(col_x):
        List.append(float((x[0:decimal])))
    # find out the c_fold symmetry and why we need to find out how many atoms in a molecule
    c_fold = int(atom_sum/(n+1))
    
    # multiply the list by c-fold symetry
    for i in range(c_fold):
        List_multi += List
        
    # attending the multiplied list to the dataframe
    data_frame['X_3D'] = List_multi
    
    # Y
    col_y = block.find_values('_atom_site_fract_y')
    List = []
    List_multi = []
    for n, y in enumerate(col_y):
        List.append(float((y[0:decimal])))
    # find out the c_fold symmetry
    c_fold = int(atom_sum/(n+1))
    
    # multiply the list by c-fold symetry
    for i in range(c_fold):
        List_multi += List
        
    # attending the multiplied list to the dataframe
    data_frame['Y_3D'] = List_multi
    
    
    
    # Z
    col_z = block.find_values('_atom_site_fract_z')
    List = []
    List_multi = []
    for n, z in enumerate(col_z):
        List.append(float((z[0:decimal])))
    # find out the c_fold symmetry
    c_fold = int(atom_sum/(n+1))
    
    # multiply the list by c-fold symetry
    for i in range(c_fold):
        List_multi += List
        
    # attending the multiplied list to the dataframe
    data_frame['Z_3D'] = List_multi
    
    
    return data_frame
