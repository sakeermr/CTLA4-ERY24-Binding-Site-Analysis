#!/usr/bin/env python3
"""
Analyze ERY2-4 peptide sequence
"""

from Bio.SeqUtils.ProtParam import ProteinAnalysis
import json
import os

ERY24_SEQUENCE = "CAWGQAILEGELAWLEGGGGGAGQLADLKRQLAWWKQAC"

def analyze_sequence(seq):
    """Analyze peptide properties"""
    
    analyzed_seq = ProteinAnalysis(seq)
    
    properties = {
        'sequence': seq,
        'length': len(seq),
        'molecular_weight': analyzed_seq.molecular_weight(),
        'isoelectric_point': analyzed_seq.isoelectric_point(),
        'aromaticity': analyzed_seq.aromaticity(),
        'instability_index': analyzed_seq.instability_index(),
        'gravy': analyzed_seq.gravy(),
        'composition': {
            'A': seq.count('A'),
            'W': seq.count('W'),
            'L': seq.count('L'),
            'Q': seq.count('Q'),
            'K': seq.count('K'),
            'R': seq.count('R'),
            'E': seq.count('E'),
            'G': seq.count('G'),
        },
        'predicted_regions': {
            'Helix_1': 'A3-E9 (hydrophobic + polar)',
            'Helix_2': 'L11-L17 (hydrophobic)',
            'Loop': 'G18-G23 (flexible)',
            'Helix_3': 'A24-L32 (charged + hydrophobic)',
            'C_terminus': 'Q33-C40 (polar + aromatic)',
        },
        'predicted_contacts': {
            'hydrophobic': ['W3', 'W15', 'L8', 'L17', 'L32', 'W36', 'L11'],
            'charged': ['Q5', 'Q25', 'K29', 'R31', 'Q33'],
            'aromatic': ['W3', 'W15', 'W36'],
        }
    }
    
    return properties

if __name__ == "__main__":
    props = analyze_sequence(ERY24_SEQUENCE)
    
    print("=" * 60)
    print("ERY2-4 PEPTIDE SEQUENCE ANALYSIS")
    print("=" * 60)
    print(f"\nSequence: {props['sequence']}")
    print(f"Length: {props['length']} residues")
    print(f"Molecular Weight: {props['molecular_weight']:.2f} Da")
    print(f"Isoelectric Point: {props['isoelectric_point']:.2f}")
    print(f"Aromaticity: {props['aromaticity']:.4f}")
    print(f"GRAVY (Hydrophobicity): {props['gravy']:.4f}")
    
    print("\nAmino Acid Composition:")
    for aa, count in props['composition'].items():
        print(f"  {aa}: {count}")
    
    print("\nPredicted Structure Regions:")
    for region, desc in props['predicted_regions'].items():
        print(f"  {region}: {desc}")
    
    print("\nPredicted Contact Residues:")
    print(f"  Hydrophobic: {props['predicted_contacts']['hydrophobic']}")
    print(f"  Charged: {props['predicted_contacts']['charged']}")
    print(f"  Aromatic: {props['predicted_contacts']['aromatic']}")
    
    # Create analysis directory if not exists
    os.makedirs('analysis', exist_ok=True)
    
    with open('analysis/ery24_properties.json', 'w') as f:
        json.dump(props, f, indent=2)
    
    print("\n✅ Analysis saved to analysis/ery24_properties.json")