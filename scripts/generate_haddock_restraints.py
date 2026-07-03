#!/usr/bin/env python3
"""
Generate HADDOCK2.4 restraints for ERY2-4 docking
Based on B7-1 binding site on CTLA-4
"""

import os
import json

# From B7-1 interface analysis
# These CTLA-4 residues interact with B7-1, so ERY2-4 should also target them
CTLA4_BINDING_SITE = [33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106]

# ERY2-4 active residues (predicted to contact CTLA-4)
ERY24_ACTIVE = [3, 8, 11, 15, 17, 25, 29, 31, 32, 36]

def generate_restraints():
    """Generate CNS-format restraint file for HADDOCK"""
    
    print("Generating HADDOCK2.4 restraints...")
    print("Based on B7-1/CTLA-4 interface from PDB 1I8L")
    
    # Create config directory
    os.makedirs('config', exist_ok=True)
    
    # Create restraint file
    restraints = []
    
    # Header
    restraints.append("! HADDOCK restraints for ERY2-4 peptide to CTLA-4")
    restraints.append("! Template: B7-1 binding site on CTLA-4 (PDB 1I8L)")
    restraints.append("! Active residues (ERY2-4): " + str(ERY24_ACTIVE))
    restraints.append("! Passive residues (CTLA-4 binding site): " + str(CTLA4_BINDING_SITE))
    restraints.append("")
    
    # Ambiguous interaction restraints (AIR)
    restraints.append("! Ambiguous Interaction Restraints (AIR)")
    restraints.append("! Contact distance: 2.0-5.0 Angstrom")
    restraints.append("")
    
    for active_res in ERY24_ACTIVE:
        restraint_line = (
            "assi (segid A and resi " + str(active_res) + " and name CB) " +
            "(segid B and (resi "
        )
        
        passive_list = " or resi ".join(map(str, CTLA4_BINDING_SITE))
        restraint_line += passive_list + ") and name CB)"
        
        restraint_line += " 2.0 2.0 2.0"
        
        restraints.append(restraint_line)
    
    restraints.append("")
    
    # Save restraints
    with open('config/ery24_restraints.tbl', 'w') as f:
        f.write("\n".join(restraints) + "\n")
    
    print("Restraints saved to config/ery24_restraints.tbl")
    print("   Active residues (ERY2-4): " + str(len(ERY24_ACTIVE)))
    print("   CTLA-4 binding site residues: " + str(len(CTLA4_BINDING_SITE)))
    
    # Also create a summary JSON
    summary = {
        'template': 'B7-1/CTLA-4 interface from PDB 1I8L',
        'receptor_chain': 'C',
        'ligand_chain': 'A (B7-1 for reference)',
        'docking_ligand': 'ERY2-4 (generated)',
        'ctla4_binding_site': CTLA4_BINDING_SITE,
        'ery24_active_residues': ERY24_ACTIVE,
        'distance_cutoff_angstrom': 5.0,
    }
    
    with open('config/restraints_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nRestraints summary saved to config/restraints_summary.json")

if __name__ == "__main__":
    generate_restraints()