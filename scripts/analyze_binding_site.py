import os
import gzip
import glob
from Bio.PDB import PDBParser
import numpy as np

def dist(a, b):
    return np.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

search = "results/haddock3_run_2/09_seletopclusts"
gz_file = os.path.join(search, "cluster_1_model_1.pdb.gz")

if not os.path.exists(gz_file):
    print("Not found: " + gz_file)
    raise SystemExit

# Decompress to a temp plain PDB
plain_file = "results/cluster_1_model_1.pdb"
with gzip.open(gz_file, 'rt') as fin:
    data = fin.read()
with open(plain_file, 'w') as fout:
    fout.write(data)

print("Analyzing: " + gz_file)
print("")

parser = PDBParser(QUIET=True)
structure = parser.get_structure("complex", plain_file)
model = structure[0]

chains = [c.get_id() for c in model]
print("Chains in model: " + str(chains))

receptor = model["A"]
peptide = model["B"]

cutoff = 4.5
ctla4_contacts = {}
contact_pairs = []

for res_r in receptor.get_residues():
    if res_r.get_id()[0] != " ":
        continue
    for res_p in peptide.get_residues():
        if res_p.get_id()[0] != " ":
            continue
        mind = 999.0
        for a in res_r.get_atoms():
            for b in res_p.get_atoms():
                d = dist(a.coord, b.coord)
                if d < mind:
                    mind = d
        if mind <= cutoff:
            rnum = res_r.get_id()[1]
            ctla4_contacts[rnum] = res_r.get_resname()
            contact_pairs.append((rnum, res_r.get_resname(),
                                  res_p.get_id()[1], res_p.get_resname(),
                                  round(mind, 2)))

ctla4_site = sorted(ctla4_contacts.keys())

print("")
print("="*55)
print("ERY2-4 BINDING SITE ON CTLA-4 (predicted)")
print("="*55)
print("CTLA-4 contact residues (within 4.5 A):")
for rnum in ctla4_site:
    print("  " + str(rnum) + " " + ctla4_contacts[rnum])

print("")
print("Total CTLA-4 contact residues: " + str(len(ctla4_site)))
print("Residue list: " + str(ctla4_site))

b7_site = [33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106]
overlap = sorted(set(ctla4_site) & set(b7_site))
print("")
print("="*55)
print("COMPARISON WITH B7-1 BINDING SITE")
print("="*55)
print("B7-1 site residues:   " + str(b7_site))
print("ERY2-4 site residues: " + str(ctla4_site))
print("Shared residues:      " + str(overlap))
if len(ctla4_site) > 0:
    pct = 100.0 * len(overlap) / len(ctla4_site)
    print("Overlap: " + str(len(overlap)) + " residues (" + str(round(pct,1)) + "% of ERY2-4 site)")

with open("results/ery24_binding_site_final.txt", "w") as f:
    f.write("ERY2-4 Binding Site on CTLA-4\n")
    f.write("Model: cluster_1_model_1 (HADDOCK score -61.1, 10 models)\n\n")
    f.write("CTLA-4 contact residues: " + str(ctla4_site) + "\n\n")
    f.write("Detailed contacts (CTLA4_res -- ERY24_res -- dist):\n")
    for cp in sorted(contact_pairs):
        f.write("  CTLA-4 " + str(cp[0]) + cp[1] + "  --  ERY2-4 " + str(cp[2]) + cp[3] + "  " + str(cp[4]) + " A\n")
    f.write("\nB7-1 site: " + str(b7_site) + "\n")
    f.write("Shared with B7-1: " + str(overlap) + "\n")

print("")
print("Saved to results/ery24_binding_site_final.txt")