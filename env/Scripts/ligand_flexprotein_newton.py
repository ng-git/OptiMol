#!/usr/bin/env python
# (C) 2017 OpenEye Scientific Software Inc. All rights reserved.
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

import sys

from openeye import oechem
from openeye import oeszybki


def main(args):
    if len(args) != 4:
        oechem.OEThrow.Usage("%s protein input_ligand output_ligand" % args[0])

    pfs = oechem.oemolistream()
    if not pfs.open(args[1]):
        oechem.OEThrow.Fatal("Unable to open %s for reading" % args[1])

    lfs = oechem.oemolistream()
    if not lfs.open(args[2]):
        oechem.OEThrow.Fatal("Unable to open %s for reading" % args[2])

    ofs = oechem.oemolostream()
    if not ofs.open(args[3]):
        oechem.OEThrow.Fatal("Unable to open %s for writing" % args[3])

    mol = oechem.OEGraphMol()
    protein = oechem.OEGraphMol()
    oechem.OEReadMolecule(lfs, mol)
    oechem.OEReadMolecule(pfs, protein)

    opts = oeszybki.OESzybkiOptions()
    opts.GetOptOptions().SetOptimizerType(oeszybki.OEOptType_NEWTON)
    opts.GetProteinOptions().SetProteinElectrostaticModel(
                             oeszybki.OEProteinElectrostatics_ExactCoulomb)
    opts.GetProteinOptions().SetProteinFlexibilityType(oeszybki.OEProtFlex_Residues)
    opts.GetProteinOptions().SetProteinFlexibilityRange(2.0)

    sz = oeszybki.OESzybki(opts)
    sz.SetProtein(protein)

    res = oeszybki.OESzybkiResults()
    if (sz(mol, res)):
        oechem.OEWriteMolecule(ofs, mol)
        res.Print(oechem.oeout)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))