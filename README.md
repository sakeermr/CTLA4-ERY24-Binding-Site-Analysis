# ERY2-4 / CTLA-4 Binding Site Analysis

Computational prediction of the binding site of the **ERY2-4** helix-loop-helix peptide on **CTLA-4**, using restraint-guided and blind molecular docking (HADDOCK3).

## Background
ERY2-4 (Ramanayake et al., *ACS Chem. Biol.* 2020, 15, 360-368) binds CTLA-4 (KD ~197 nM) and competitively inhibits the CTLA-4/B7-1 interaction (IC50 ~1.1 uM). Its binding site was not determined experimentally. This project predicts it computationally.

- **Target:** CTLA-4 (chain C, PDB 1I8L)
- **Reference binder:** B7-1
- **Peptide:** ERY2-4 (\CAWGQAILEGELAWLEGGGGGAGQLADLKRQLAWWKQAC\), 3D model by AlphaFold2

## Key result
Guided docking places ERY2-4 on the B7-1 binding surface (CTLA-4 residues 95-106; 90% overlap with the B7-1 interface; HADDOCK score -61.1, 995 A^2 BSA). Blind docking localises to an adjacent patch (61-70) that also abuts the B7-1 surface. Both strategies converge on the B7-1 interface, giving structural support for the observed competitive inhibition. See \eport/\ for the full write-up.

## Method
HADDOCK3 v2026.5.0 run inside Docker. Pipeline: topology -> rigid-body -> flexible refinement -> energy minimisation -> FCC clustering -> CAPRI evaluation.

## Reproduce
\\\
# 1. Build the docking container
docker build -t haddock3-ery24:latest .

# 2. Prepare structures & restraints
python scripts/analyze_ery24_sequence.py
python scripts/extract_b7_interface.py
python scripts/prepare_ctla4_receptor.py
python scripts/fix_chains.py
python scripts/generate_haddock_restraints.py

# 3. Run guided docking
python scripts/run_haddock3_docker.py

# 4. Analyse
python scripts/analyze_binding_site.py
python scripts/tiebreaker.py
python scripts/make_figure.py
\\\

## Repository layout
- \scripts/\ - analysis and docking scripts
- \config/\ - HADDOCK restraints and workflow configs
- \structures/\ - receptor and peptide input PDBs
- \eport/\ - final PDF report, figure, and summary
- \Dockerfile\ - HADDOCK3 container definition

## Note
This is a computational prediction. Confidence level: a well-supported, experimentally-consistent hypothesis, to be confirmed by mutagenesis (e.g. CTLA-4 Y104A/Y105A).
