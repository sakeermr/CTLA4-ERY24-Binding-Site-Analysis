import os
import gzip
import glob
from Bio.PDB import PDBParser
import numpy as np

def dist(a, b):
    return np.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

search = "results/haddock3_abinitio/09_seletopclusts"

# Analyze the top 3 clusters' first model
b7_site = [33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106]
ery24_guided_site = [95, 97, 98, 99, 100, 102, 103, 104, 105, 106]  # from restraint-guided run

def get_site(gz_path):
    tmp = "results/_tmp_abinitio.pdb"
    with gzip.open(gz_path, 'rt') as fin:
        data = fin.read()
    with open(tmp, 'w') as fout:
        fout.write(data)
    parser = PDBParser(QUIET=True)
    st = parser.get_structure("c", tmp)[0]
    chains = [c.get_id() for c in st]
    if "A" not in st or "B" not in st:
        return None, chains
    rec, pep = st["A"], st["B"]
    site = set()
    for rr in rec.get_residues():
        if rr.get_id()[0] != " ":
            continue
        for rp in pep.get_residues():
            if rp.get_id()[0] != " ":
                continue
            mind = 999.0
            for a in rr.get_atoms():
                for b in rp.get_atoms():
                    d = dist(a.coord, b.coord)
                    if d < mind:
                        mind = d
            if mind <= 4.5:
                site.add(rr.get_id()[1])
                break
    return sorted(site), chains

print("="*60)
print("AB-INITIO (BLIND) DOCKING - binding site analysis")
print("="*60)
print("")

for cn in [1, 2, 3]:
    gz = os.path.join(search, "cluster_" + str(cn) + "_model_1.pdb.gz")
    if not os.path.exists(gz):
        print("Cluster " + str(cn) + ": (not found)")
        continue
    site, chains = get_site(gz)
    if site is None:
        print("Cluster " + str(cn) + ": chains present = " + str(chains) + " (need A and B)")
        continue
    ov_b7 = sorted(set(site) & set(b7_site))
    ov_guided = sorted(set(site) & set(ery24_guided_site))
    pct_b7 = 100.0*len(ov_b7)/len(site) if site else 0
    print("CLUSTER " + str(cn) + ":")
    print("  CTLA-4 contact residues: " + str(site))
    print("  Overlap with B7-1 site:  " + str(len(ov_b7)) + "/" + str(len(site)) + " (" + str(round(pct_b7,1)) + "%) -> " + str(ov_b7))
    print("  Overlap with guided run: " + str(len(ov_guided)) + " residues -> " + str(ov_guided))
    print("")

with open("results/abinitio_binding_site.txt", "w") as f:
    f.write("Ab-initio (blind) docking - top cluster binding sites\n")
    for cn in [1, 2, 3]:
        gz = os.path.join(search, "cluster_" + str(cn) + "_model_1.pdb.gz")
        if os.path.exists(gz):
            site, _ = get_site(gz)
            f.write("Cluster " + str(cn) + ": " + str(site) + "\n")
    f.write("\nB7-1 site: " + str(b7_site) + "\n")
    f.write("Guided-run site: " + str(ery24_guided_site) + "\n")

print("Saved to results/abinitio_binding_site.txt")