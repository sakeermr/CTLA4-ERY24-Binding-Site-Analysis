import os

def set_chain(infile, outfile, new_chain, strip_model=False):
    lines_out = []
    for line in open(infile):
        if strip_model and (line.startswith("MODEL") or line.startswith("ENDMDL")):
            continue
        if line.startswith("ATOM") or line.startswith("HETATM"):
            # chain ID is column 22 (index 21)
            line = line[:21] + new_chain + line[22:]
        lines_out.append(line)
    with open(outfile, "w") as f:
        f.writelines(lines_out)
    print("Wrote " + outfile + " with chain " + new_chain)

# Receptor CTLA-4 -> chain A
set_chain("structures/ctla4_receptor.pdb", "structures/ctla4_A.pdb", "A")

# Peptide ERY2-4 -> chain B (also strip MODEL/ENDMDL lines)
set_chain("structures/ery24_alphafold.pdb", "structures/ery24_B.pdb", "B", strip_model=True)

print("Done.")