from Bio.PDB import PDBParser, PDBIO, Select
import numpy as np

# Binding-site residues from the two docking strategies
guided_residues = [95, 97, 98, 99, 100, 102, 103, 104, 105, 106]   # restraint-guided
blind_residues  = [16, 61, 62, 63, 64, 65, 66, 68, 69, 70, 82, 127] # blind (ab initio)

parser = PDBParser(QUIET=True)
structure = parser.get_structure('ctla4', 'structures/ctla4_A.pdb')
chain = structure[0]['A']

# build a lookup of residues present
present = {}
for res in chain.get_residues():
    if res.get_id()[0] == ' ':
        present[res.get_id()[1]] = res

def report(name, residues):
    print('')
    print('='*72)
    print(name)
    print('='*72)
    print('resid  resname   CA_x       CA_y       CA_z')
    print('-'*72)
    cas = []
    rows = []
    for rnum in residues:
        if rnum in present:
            res = present[rnum]
            rn = res.get_resname()
            if 'CA' in res:
                c = res['CA'].coord
                cas.append(c)
                print(str(rnum).rjust(4) + '   ' + rn + '   ' + 
                      str(round(float(c[0]),3)).rjust(9) + '  ' +
                      str(round(float(c[1]),3)).rjust(9) + '  ' +
                      str(round(float(c[2]),3)).rjust(9))
                rows.append((rnum, rn, c))
        else:
            print(str(rnum).rjust(4) + '   (not found in structure)')
    if cas:
        cen = np.mean(cas, axis=0)
        print('-'*72)
        print('CENTROID (mean of CA):  x=' + str(round(float(cen[0]),3)) +
              '  y=' + str(round(float(cen[1]),3)) +
              '  z=' + str(round(float(cen[2]),3)))
    return rows, (cen if cas else None)

print('Reference frame: PDB 1I8L, CTLA-4 (chain relabelled A)')
print('Coordinates in Angstroms')

g_rows, g_cen = report('GUIDED SITE (restraint-guided docking): residues 95-106', guided_residues)
b_rows, b_cen = report('BLIND SITE (ab-initio docking): residues 61-70 region', blind_residues)

# Save combined CSV (all atoms, both sites)
with open('results/both_sites_coordinates.csv', 'w') as f:
    f.write('site,residue,resnum,atom,x,y,z\n')
    for label, residues in [('guided', guided_residues), ('blind', blind_residues)]:
        for rnum in residues:
            if rnum in present:
                res = present[rnum]
                for atom in res.get_atoms():
                    c = atom.coord
                    f.write(label + ',' + res.get_resname() + ',' + str(rnum) + ',' +
                            atom.get_name() + ',' + str(round(float(c[0]),3)) + ',' +
                            str(round(float(c[1]),3)) + ',' + str(round(float(c[2]),3)) + '\n')

# Save each site as its own PDB fragment (openable in Maestro/PyMOL)
class Sel(Select):
    def __init__(self, res): self.res = res
    def accept_residue(self, residue): return residue.get_id()[1] in self.res

io = PDBIO(); io.set_structure(structure)
io.save('results/guided_site_95-106.pdb', Sel(guided_residues))
io.save('results/blind_site_61-70.pdb', Sel(blind_residues))

print('')
print('='*72)
print('Saved files:')
print('  results/both_sites_coordinates.csv    (all atoms, both sites, x/y/z)')
print('  results/guided_site_95-106.pdb        (guided-site residues)')
print('  results/blind_site_61-70.pdb          (blind-site residues)')
print('='*72)
