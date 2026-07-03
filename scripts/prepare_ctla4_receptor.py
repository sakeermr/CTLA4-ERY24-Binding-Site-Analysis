#!/usr/bin/env python3
"""
Prepare CTLA-4 receptor from PDB 1I8L
"""

from Bio.PDB import PDBParser, PDBIO, Select
import os

class ChainSelector(Select):
    """Select specific chain"""
    def __init__(self, chain_id):
        self.chain_id = chain_id
    
    def accept_chain(self, chain):
        return chain.get_id() == self.chain_id

def prepare_receptor():
    """Extract CTLA-4 chain C from 1I8L"""
    
    print("🔧 Preparing CTLA-4 receptor...")
    
    # Create structures directory
    os.makedirs('structures', exist_ok=True)
    
    # Parse structure
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('1I8L', 'data/pdb/1I8L.pdb')
    
    # Save only CTLA-4 chain
    io = PDBIO()
    io.set_structure(structure)
    io.save('structures/ctla4_receptor.pdb', ChainSelector('C'))
    
    print("✅ CTLA-4 receptor saved to structures/ctla4_receptor.pdb")

if __name__ == "__main__":
    prepare_receptor()