#!/usr/bin/env python3
"""
Extract B7-1 binding site on CTLA-4 from PDB 1I8L
Automatically find which chains interact
"""

from Bio.PDB import PDBParser
import numpy as np
import pandas as pd
import urllib.request
import os

def calculate_distance(coord1, coord2):
    """Calculate Euclidean distance between two coordinates"""
    return np.sqrt(sum((coord1[i] - coord2[i])**2 for i in range(3)))

def download_pdb():
    """Download PDB 1I8L if not exists"""
    pdb_file = 'data/pdb/1I8L.pdb'
    
    if not os.path.exists(pdb_file):
        print("Downloading PDB 1I8L...")
        url = "https://files.rcsb.org/download/1I8L.pdb"
        urllib.request.urlretrieve(url, pdb_file)
        print("Downloaded")
    
    return pdb_file

def find_interacting_chains(pdb_file, distance_cutoff=5.0):
    """Find which chains interact with each other"""
    
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('1I8L', pdb_file)
    model = structure[0]
    
    # Get all chains
    chains = list(model.get_chains())
    chain_ids = [chain.get_id() for chain in chains]
    
    print("\nTrying all chain combinations...")
    print("Looking for chains that interact within " + str(distance_cutoff) + " A")
    
    best_pair = None
    best_contact_count = 0
    
    # Try all pairs of chains
    for i, chain1 in enumerate(chains):
        for chain2 in chains[i+1:]:
            chain1_id = chain1.get_id()
            chain2_id = chain2.get_id()
            
            # Count contacts between these chains
            contact_count = 0
            
            for res1 in chain1.get_residues():
                if res1.get_id()[0] != ' ':
                    continue
                
                for res2 in chain2.get_residues():
                    if res2.get_id()[0] != ' ':
                        continue
                    
                    # Check minimum distance
                    min_dist = float('inf')
                    for atom1 in res1.get_atoms():
                        for atom2 in res2.get_atoms():
                            dist = calculate_distance(atom1.coord, atom2.coord)
                            if dist < min_dist:
                                min_dist = dist
                    
                    if min_dist <= distance_cutoff:
                        contact_count += 1
            
            if contact_count > 0:
                print("  Chains " + chain1_id + "-" + chain2_id + ": " + str(contact_count) + " contacts")
                
                if contact_count > best_contact_count:
                    best_contact_count = contact_count
                    best_pair = (chain1_id, chain2_id)
    
    if best_pair:
        print("\nBest match: Chains " + best_pair[0] + "-" + best_pair[1] + " with " + str(best_contact_count) + " contacts")
        return best_pair
    else:
        print("\nNo interacting chains found!")
        return None

def extract_interface(pdb_file, chain_receptor, chain_ligand, distance_cutoff=5.0):
    """Extract interface residues between two chains"""
    
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('1I8L', pdb_file)
    model = structure[0]
    
    receptor = model[chain_receptor]
    ligand = model[chain_ligand]
    
    contacts = []
    
    for res_r in receptor.get_residues():
        if res_r.get_id()[0] != ' ':
            continue
        
        for res_l in ligand.get_residues():
            if res_l.get_id()[0] != ' ':
                continue
            
            min_dist = float('inf')
            contact_type = None
            
            for atom_r in res_r.get_atoms():
                for atom_l in res_l.get_atoms():
                    dist = calculate_distance(atom_r.coord, atom_l.coord)
                    if dist < min_dist:
                        min_dist = dist
                        contact_type = str(atom_r.name) + "-" + str(atom_l.name)
            
            if min_dist <= distance_cutoff:
                contacts.append({
                    'receptor_resnum': res_r.get_id()[1],
                    'receptor_resname': res_r.get_resname(),
                    'ligand_resnum': res_l.get_id()[1],
                    'ligand_resname': res_l.get_resname(),
                    'distance': min_dist,
                    'contact_atoms': contact_type,
                })
    
    return pd.DataFrame(contacts)

if __name__ == "__main__":
    # Create analysis directory
    os.makedirs('analysis', exist_ok=True)
    
    # Download PDB
    pdb_file = download_pdb()
    
    print("\n" + "="*60)
    print("EXTRACTING B7-1 BINDING SITE ON CTLA-4")
    print("="*60)
    
    # Find interacting chains
    chain_pair = find_interacting_chains(pdb_file, distance_cutoff=5.0)
    
    if chain_pair:
        chain_receptor, chain_ligand = chain_pair
        
        print("\nExtracting detailed interface...")
        contacts_df = extract_interface(pdb_file, chain_receptor, chain_ligand, distance_cutoff=5.0)
        
        print("\nFound " + str(len(contacts_df)) + " contact residue pairs")
        
        # Get unique residues
        receptor_residues = sorted(contacts_df['receptor_resnum'].unique())
        ligand_residues = sorted(contacts_df['ligand_resnum'].unique())
        
        print("\nChain " + chain_receptor + " contact residues: " + str(list(receptor_residues)))
        print("Chain " + chain_ligand + " contact residues: " + str(list(ligand_residues)))
        
        # Save detailed contacts
        contacts_df.to_csv('analysis/b7_ctla4_contacts.csv', index=False)
        print("\nSaved to analysis/b7_ctla4_contacts.csv")
        
        # Save residue list
        with open('analysis/b7_binding_site.txt', 'w') as f:
            f.write("CTLA-4 (Chain " + chain_receptor + ") residues in interface:\n")
            f.write(str(list(receptor_residues)))
            f.write("\n\nB7-1 (Chain " + chain_ligand + ") residues in interface:\n")
            f.write(str(list(ligand_residues)))
        
        print("Saved to analysis/b7_binding_site.txt")
    else:
        print("\nNo interacting chains found with cutoff 5.0 A")
        print("Using dummy output files...")
        
        with open('analysis/b7_ctla4_contacts.csv', 'w') as f:
            f.write("No direct contacts found\n")
        
        with open('analysis/b7_binding_site.txt', 'w') as f:
            f.write("No binding site detected\n")