#!/usr/bin/env python
# (C) 2018 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

#############################################################################
# Superposition of a fit protein on to a reference protein using a
# shape-based fit of the secondary structure elements.
#############################################################################
import sys
import os
import tempfile
from openeye import oechem
from openeye import oespruce


def ReadProteinFromPDB(pdb_file, mol):
    ifs = oechem.oemolistream()
    ifs.SetFlavor(oechem.OEFormat_PDB, oechem.OEIFlavor_PDB_Default | oechem.OEIFlavor_PDB_DATA | oechem.OEIFlavor_PDB_ALTLOC)  # noqa

    if not ifs.open(pdb_file):
        oechem.OEThrow.Fatal("Unable to open %s for reading." % pdb_file)

    temp_mol = oechem.OEGraphMol()
    if not oechem.OEReadMolecule(ifs, temp_mol):
        oechem.OEThrow.Fatal("Unable to read molecule from %s." % pdb_file)
    ifs.close()

    fact = oechem.OEAltLocationFactory(temp_mol)
    mol.Clear()
    fact.MakePrimaryAltMol(mol)
    return (mol)


def main(argv=[__name__]):
    if len(argv) not in [3, 4]:
        oechem.OEThrow.Usage("%s <reference protein PDB> <fit protein PDB> [nowrite]" % argv[0])  # noqa

    do_write = True
    if len(argv) == 4:
        if argv[3] != "nowrite":
            oechem.OEThrow.Warning("%s is not a valid option.\n" % argv[3])
            sys.exit(1)
        else:
            do_write = False

    ref_prot_file = argv[1]
    fit_prot_file = argv[2]

    ref_prot = oechem.OEGraphMol()
    fit_prot = oechem.OEGraphMol()

    ref_success = ReadProteinFromPDB(ref_prot_file, ref_prot)
    fit_success = ReadProteinFromPDB(fit_prot_file, fit_prot)

    if (not ref_success) or (not fit_success):
        oechem.OEThrow.Fatal("Unable to protein(s) from PDB file.")

    superposition = oespruce.OESecondaryStructureSuperposition(ref_prot, fit_prot)  # noqa
    tanimoto = superposition.GetTanimoto()

    superposition.Transform(fit_prot)

    pdb_ext = ".pdb"
    str_pos = fit_prot_file.find(pdb_ext)
    base_name = fit_prot_file[0:str_pos]
    temp_dir = tempfile.mkdtemp()
    output_fit_file = os.path.join(temp_dir, base_name + "_sp.oeb.gz")

    print("Tanimoto score for the secondary structure fit of",
          fit_prot_file, "to", ref_prot_file, "is", tanimoto, ".\n")
    print("Writing superimposed fit protein to", output_fit_file)

    if do_write:
        ofs = oechem.oemolostream(output_fit_file)
        oechem.OEWriteMolecule(ofs, fit_prot)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
