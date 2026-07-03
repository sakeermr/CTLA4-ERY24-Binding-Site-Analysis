#!/usr/bin/env python3
"""
Generate ERY2-4 3D structure from sequence
"""

import os

ERY24_SEQUENCE = "CAWGQAILEGELAWLEGGGGGAGQLADLKRQLAWWKQAC"

def generate_ery24_pdb():
    """Generate ERY2-4 structure using simple backbone"""
    
    print("🔨 Building ERY2-4 3D structure...")
    
    aa_codes = {
        'C': 'CYS', 'A': 'ALA', 'W': 'TRP', 'G': 'GLY', 'Q': 'GLN',
        'I': 'ILE', 'L': 'LEU', 'E': 'GLU', 'D': 'ASP', 'K': 'LYS',
        'R': 'ARG',
    }
    
    # Create PDB file with backbone coordinates
    pdb_lines = [
        "REMARK   1  ERY2-4 PEPTIDE GENERATED STRUCTURE",
        "REMARK   1  SEQUENCE: CAWGQAILEGELAWLEGGGGGAGQLADLKRQLAWWKQAC",
    ]
    
    atom_num = 1
    for i, aa in enumerate(ERY24_SEQUENCE, 1):
        res_code = aa_codes.get(aa, 'ALA')
        
        # Generate backbone atoms
        x = i * 3.8
        y = 0.0 + (i % 2) * 1.5
        z = 0.0
        
        # N atom
        pdb_lines.append(
            f"ATOM  {atom_num:5d}  N   {res_code} A{i:4d}    "
            f"{x-1.45:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           N"
        )
        atom_num += 1
        
        # CA atom
        pdb_lines.append(
            f"ATOM  {atom_num:5d}  CA  {res_code} A{i:4d}    "
            f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C"
        )
        atom_num += 1
        
        # C atom
        pdb_lines.append(
            f"ATOM  {atom_num:5d}  C   {res_code} A{i:4d}    "
            f"{x+1.24:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C"
        )
        atom_num += 1
        
        # O atom
        pdb_lines.append(
            f"ATOM  {atom_num:5d}  O   {res_code} A{i:4d}    "
            f"{x+2.34:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           O"
        )
        atom_num += 1
    
    pdb_lines.append("END")
    
    # Create structures directory
    os.makedirs('structures', exist_ok=True)
    
    # Write PDB file
    pdb_content = "\n".join(pdb_lines) + "\n"
    
    with open('structures/ery24_initial.pdb', 'w') as f:
        f.write(pdb_content)
    
    print(f"✅ Initial structure written to structures/ery24_initial.pdb")
    print(f"   Length: {len(ERY24_SEQUENCE)} residues")
    print(f"   Atoms: {atom_num-1}")

if __name__ == "__main__":
    generate_ery24_pdb()