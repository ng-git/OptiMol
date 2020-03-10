import sys
from gemmi import cif

#This script reads cif file and prints out the elements it contains
greeted = set()
for path in sys.argv[1:]:
    try:
        doc = cif.read_file('filename.cif')  # copy all the data from mmCIF file
        block = doc.sole_block()  # mmCIF has exactly one block
        for element in block.find_loop("_atom_site_type_symbol"): #name modified according to CIF file content
            if element not in greeted:
                print("Hello " + element)
                greeted.add(element)
    except Exception as e:
        print("Oops. %s" % e)
        sys.exit(1)
