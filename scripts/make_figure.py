import gzip
import numpy as np
from Bio.PDB import PDBParser
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def dist(a, b):
    return np.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

gz = 'results/haddock3_run_2/09_seletopclusts/cluster_1_model_1.pdb.gz'
tmp = 'results/_fig_model.pdb'
with gzip.open(gz, 'rt') as f:
    open(tmp, 'w').write(f.read())

parser = PDBParser(QUIET=True)
model = parser.get_structure('c', tmp)[0]
rec, pep = model['A'], model['B']

ctla4_res = [95, 97, 98, 99, 100, 102, 103, 104, 105, 106]
aa = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}

pep_contacts = {}
matrix = {}
for rr in rec.get_residues():
    rn = rr.get_id()[1]
    if rn not in ctla4_res:
        continue
    for rp in pep.get_residues():
        pn = rp.get_id()[1]
        mind = 999
        for a in rr.get_atoms():
            for b in rp.get_atoms():
                d = dist(a.coord, b.coord)
                if d < mind:
                    mind = d
        if mind <= 4.5:
            matrix[(rn, pn)] = mind
            pep_contacts[pn] = rp.get_resname()

pep_res = sorted(pep_contacts.keys())
ctla4_labels = []
for rn in ctla4_res:
    for rr in rec.get_residues():
        if rr.get_id()[1] == rn:
            ctla4_labels.append(aa.get(rr.get_resname(),'X') + str(rn))
            break
pep_labels = [aa.get(pep_contacts[pn],'X') + str(pn) for pn in pep_res]

fig, ax = plt.subplots(figsize=(9, 6))
for i, rn in enumerate(ctla4_res):
    for j, pn in enumerate(pep_res):
        if (rn, pn) in matrix:
            d = matrix[(rn, pn)]
            color = plt.cm.YlOrRd(1.0 - (d - 1.5) / 3.5)
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=color, edgecolor='white', linewidth=1.5))
            ax.text(j+0.5, i+0.5, str(round(d,1)), ha='center', va='center', fontsize=7)

ax.set_xlim(0, len(pep_res))
ax.set_ylim(0, len(ctla4_res))
ax.set_xticks([j+0.5 for j in range(len(pep_res))])
ax.set_xticklabels(pep_labels, rotation=45, ha='right', fontsize=9)
ax.set_yticks([i+0.5 for i in range(len(ctla4_res))])
ax.set_yticklabels(ctla4_labels, fontsize=9)
ax.set_xlabel('ERY2-4 peptide residues', fontsize=11, fontweight='bold')
ax.set_ylabel('CTLA-4 binding-site residues', fontsize=11, fontweight='bold')
ax.set_title('ERY2-4 / CTLA-4 interface contact map (4.5 A)\nHADDOCK3 top cluster, score -61.1', fontsize=12, fontweight='bold')
ax.invert_yaxis()
ax.set_aspect('equal')
sm = plt.cm.ScalarMappable(cmap=plt.cm.YlOrRd_r, norm=plt.Normalize(vmin=1.5, vmax=5.0))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.04)
cbar.set_label('contact distance (A)', fontsize=9)
plt.tight_layout()
plt.savefig('results/ERY24_contact_map.png', dpi=200, bbox_inches='tight')
print('Saved results/ERY24_contact_map.png')
print('Contacts plotted:', len(matrix))
