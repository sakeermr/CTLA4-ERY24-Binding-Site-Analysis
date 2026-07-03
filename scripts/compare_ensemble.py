import os
import gzip
from Bio.PDB import PDBParser
import numpy as np

def dist(a, b):
    return np.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

def get_site(run_dir):
    gz = os.path.join(run_dir, "09_seletopclusts", "cluster_1_model_1.pdb.gz")
    if not os.path.exists(gz):
        return None
    tmp = "results/_tmp_model.pdb"
    with gzip.open(gz, 'rt') as fin:
        data = fin.read()
    with open(tmp, 'w') as fout:
        fout.write(data)
    parser = PDBParser(QUIET=True)
    st = parser.get_structure("c", tmp)[0]
    if "A" not in st or "B" not in st:
        return None
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
    return sorted(site)

runs = {
    "Run_2 (main)": "results/haddock3_run_2",
    "Replicate 2":  "results/haddock3_run_seed2",
    "Replicate 3":  "results/haddock3_run_seed3",
    "Replicate 4":  "results/haddock3_run_seed4",
}

b7_site = [33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106]

print("="*60)
print("ENSEMBLE CONVERGENCE - ERY2-4 binding site on CTLA-4")
print("="*60)

all_sites = {}
for name, rd in runs.items():
    site = get_site(rd)
    all_sites[name] = site
    if site is None:
        print(name + ": (no result found)")
    else:
        ov = sorted(set(site) & set(b7_site))
        pct = 100.0*len(ov)/len(site) if site else 0
        print("")
        print(name + ":")
        print("  Site: " + str(site))
        print("  B7-1 overlap: " + str(len(ov)) + "/" + str(len(site)) + " (" + str(round(pct,1)) + "%)")

# Residues found in ALL runs
valid = [s for s in all_sites.values() if s]
if len(valid) >= 2:
    consensus = set(valid[0])
    for s in valid[1:]:
        consensus &= set(s)
    consensus = sorted(consensus)
    print("")
    print("="*60)
    print("CONSENSUS (residues contacted in ALL " + str(len(valid)) + " runs):")
    print("  " + str(consensus))
    ov = sorted(set(consensus) & set(b7_site))
    print("  These are ALL in B7-1 site: " + str(set(consensus).issubset(set(b7_site))))
    print("="*60)

    with open("results/ensemble_consensus.txt", "w") as f:
        f.write("ERY2-4 / CTLA-4 Ensemble Convergence\n")
        f.write("="*45 + "\n\n")
        for name, site in all_sites.items():
            f.write(name + ": " + str(site) + "\n")
        f.write("\nConsensus (all runs): " + str(consensus) + "\n")
        f.write("B7-1 site: " + str(b7_site) + "\n")
    print("")
    print("Saved to results/ensemble_consensus.txt")