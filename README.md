# ERY2-4 / CTLA-4 Binding Site Analysis

Computational prediction of the binding site of the **ERY2-4** helix-loop-helix (HLH) peptide on the immune checkpoint receptor **CTLA-4**, using restraint-guided and blind molecular docking with **HADDOCK3**, an **AlphaFold2** peptide model, and the CTLA-4/B7-1 crystal structure (PDB **1I8L**) as reference.

---

## Table of Contents
1. [Background](#background)
2. [Objective](#objective)
3. [Key Result](#key-result)
4. [Methods](#methods)
5. [Repository Structure](#repository-structure)
6. [How to Reproduce](#how-to-reproduce)
7. [Detailed Results](#detailed-results)
8. [Limitations & Confidence](#limitations--confidence)
9. [Suggested Next Steps](#suggested-next-steps)
10. [References](#references)

---

## Background

CTLA-4 (Cytotoxic T-Lymphocyte-Associated protein 4) is an inhibitory immune checkpoint receptor. It competes with the co-stimulatory receptor CD28 for the shared ligands B7-1 (CD80) and B7-2 (CD86). Blocking CTLA-4 is a validated cancer-immunotherapy strategy.

**ERY2-4** is a disulfide-cyclised helix-loop-helix peptide reported by Ramanayake et al. (*ACS Chem. Biol.* 2020, 15, 360-368). Experimentally it:

- binds human CTLA-4 with **K<sub>D</sub> ~ 197 nM**,
- **competitively inhibits** the CTLA-4/B7-1 interaction (**IC<sub>50</sub> ~ 1.1 uM**),
- is **selective for CTLA-4** over CD28.

However, the **binding site of ERY2-4 on CTLA-4 was never determined experimentally**. This project predicts it computationally.

| Item | Value |
|------|-------|
| Target protein | CTLA-4 (chain C of PDB 1I8L) |
| Natural/reference binder | B7-1 |
| Peptide | ERY2-4 (39 residues) |
| Peptide sequence | `CAWGQAILEGELAWLEGGGGGAGQLADLKRQLAWWKQAC` |
| Peptide 3D model | AlphaFold2 (ColabFold) |

---

## Objective

Predict the binding site of ERY2-4 on CTLA-4 and determine whether it overlaps the natural B7-1 ligand interface — which would provide a structural mechanism for the experimentally-observed competitive inhibition.

---

## Key Result

**Both a guided and an independent blind docking run place ERY2-4 on the B7-1 binding surface of CTLA-4 — not at a distant/allosteric site.**

- **Guided docking** (informed by the experimental competition data) localises ERY2-4 to CTLA-4 residues **95-106**, centred on the **Pro102-Pro103-Tyr104-Tyr105** ligand-recognition motif.
  - HADDOCK score **-61.1**, 10-model cluster, buried surface area **995 A^2**.
  - **90% overlap (9/10 residues)** with the B7-1 interface.
- **Blind docking** (no restraints) localises to an adjacent patch (**61-70**) that also **abuts the B7-1 surface** (contacts B7-1 residues 63/65 at 0.0 A).
- A spatial "tiebreaker" analysis confirms **neither site is distant from the B7-1 interface** — both converge on the B7-1 binding region.

This convergence, from two independent search strategies, provides structural support for the competitive-binding model: **ERY2-4 blocks CTLA-4/B7-1 engagement by binding at the B7-1 interface.**

> **Confidence level:** a well-supported, experimentally-consistent *hypothesis* — not an experimentally-determined structure. The exact contact sub-region should be confirmed by mutagenesis.

See [`report/`](report/) for the full write-up and figure.

---

## Methods

### Structure preparation
- **Receptor (CTLA-4):** extracted as chain C from PDB **1I8L** (the CTLA-4/B7-1 complex).
- **B7-1 reference interface:** computed directly from 1I8L (4.5 A heavy-atom cutoff), auto-detecting the interacting chain pair (chains A-C, 44 residue contacts). B7-1 interface residues: `33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106`.
- **Peptide (ERY2-4):** 3D model generated from sequence with **AlphaFold2** (ColabFold); top-ranked model used.
- Chains renamed so receptor = A, peptide = B for consistent restraint referencing.

### Docking
Performed with **HADDOCK3 v2026.5.0** inside a Docker container. Data-driven workflow:

```
topoaa -> rigidbody -> seletop -> flexref -> emref -> clustfcc -> seletopclusts -> caprieval
```

Two experiments:
1. **Guided:** ambiguous interaction restraints (AIRs) directing ERY2-4 toward the B7-1 region.
2. **Blind (ab-initio):** no restraints, surface-wide random-AIR sampling of 1000 rigid-body models, to test whether the same site is recovered without guidance.

### Analysis
- Interface contact extraction (Biopython, 4.5 A cutoff).
- Comparison against the B7-1 interface.
- Spatial "tiebreaker": proximity of each candidate site to the B7-1 interface.
- Contact-map figure (matplotlib).

---

## Repository Structure

```
CTLA4-ERY24-Binding-Site-Analysis/
├── README.md                     <- this file
├── Dockerfile                    <- HADDOCK3 container definition
├── docker-compose.yml
├── requirements.txt              <- Python dependencies
│
├── scripts/                      <- all analysis & docking scripts
│   ├── analyze_ery24_sequence.py     Peptide sequence properties
│   ├── extract_b7_interface.py       B7-1/CTLA-4 interface from 1I8L
│   ├── prepare_ctla4_receptor.py     Extract CTLA-4 chain
│   ├── fix_chains.py                 Rename chains (A=receptor, B=peptide)
│   ├── generate_haddock_restraints.py  Build AIR restraints
│   ├── run_haddock3_docker.py        Guided docking run
│   ├── run_abinitio.py               Blind docking run
│   ├── run_ensemble.py               Replicate runs
│   ├── analyze_binding_site.py       Extract guided binding site
│   ├── analyze_abinitio.py           Extract blind binding site
│   ├── compare_ensemble.py           Compare replicate sites
│   ├── tiebreaker.py                 Spatial proximity vs B7-1
│   └── make_figure.py                Contact-map figure
│
├── config/                       <- HADDOCK restraints & workflow configs
│   ├── ery24_restraints.tbl          AIR restraints
│   └── haddock3_workflow.cfg         Guided workflow
│
├── structures/                   <- input PDBs
│   ├── ctla4_A.pdb                   CTLA-4 receptor (chain A)
│   ├── ery24_B.pdb                   ERY2-4 peptide (chain B)
│   └── ery24_alphafold.pdb           Raw AlphaFold model
│
└── report/                       <- deliverables
    ├── ERY24_CTLA4_BindingSite_Report.pdf
    ├── ERY24_contact_map.png
    ├── ery24_binding_site_final.txt
    └── abinitio_binding_site.txt
```

> **Note:** the large HADDOCK output directories (`results/haddock3_run_*`, hundreds of MB of intermediate files) are excluded via `.gitignore`. They are fully regenerable by running the scripts below.

---

## How to Reproduce

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Python 3.10+ with Biopython, numpy, pandas (`pip install -r requirements.txt`)

### 1. Build the HADDOCK3 container
```bash
docker build -t haddock3-ery24:latest .
```

### 2. Prepare structures and restraints
```bash
python scripts/analyze_ery24_sequence.py       # peptide properties
python scripts/extract_b7_interface.py          # B7-1 interface from 1I8L
python scripts/prepare_ctla4_receptor.py        # CTLA-4 receptor
# (ERY2-4 3D model comes from AlphaFold2 / ColabFold, provided in structures/)
python scripts/fix_chains.py                     # rename chains A/B
python scripts/generate_haddock_restraints.py   # build restraints
```

### 3. Run docking
```bash
python scripts/run_haddock3_docker.py           # guided docking (~15-30 min)
python scripts/run_abinitio.py                  # blind docking (~1-2 h)
```

### 4. Analyse and visualise
```bash
python scripts/analyze_binding_site.py          # guided binding site
python scripts/analyze_abinitio.py              # blind binding site
python scripts/tiebreaker.py                    # proximity to B7-1
python scripts/make_figure.py                   # contact-map figure
```

---

## Detailed Results

### Guided docking — top cluster

| Metric | Value | Interpretation |
|--------|-------|----------------|
| HADDOCK score | -61.1 +/- 2.0 | Strongly favourable |
| Cluster size | 10 models | Well-converged |
| Buried surface area | 995 A^2 | Large interface |
| Van der Waals energy | -37.5 | Good shape complementarity |
| Electrostatic energy | -33.8 | Favourable polar contacts |
| Desolvation energy | -26.0 | Favourable |

**ERY2-4 binding site on CTLA-4:** `95, 97, 98, 99, 100, 102, 103, 104, 105, 106`

**Closest contacts:**

| CTLA-4 | ERY2-4 | Distance (A) |
|--------|--------|--------------|
| Glu97 | Gln24 | 1.74 |
| Tyr104 | Gln24 | 2.25 |
| Leu106 | Glu11 | 2.29 |
| Tyr104 | Leu8 | 2.66 |
| Tyr105 | Trp3 | 2.98 |
| Tyr105 | Ile7 | 3.01 |

The interface is dominated by CTLA-4 **Tyr104/Tyr105** and ERY2-4 **tryptophans (Trp3, Trp34, Trp35)** and **Leu8** — consistent with the conserved Leu->Trp substitution reported as critical in the original paper.

### Comparison with B7-1

| | Residues |
|--|----------|
| B7-1 interface | 33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106 |
| ERY2-4 (guided) | 95, 97, 98, 99, 100, 102, 103, 104, 105, 106 |
| **Shared** | **95, 97, 99, 100, 102, 103, 104, 105, 106 (90%)** |

### Blind (ab-initio) docking
- Top cluster score **-53.5**, 4 models, strong electrostatics (-102).
- Localises to CTLA-4 residues **16, 61-70, 82, 127**.
- Overlaps B7-1 by 2 residues (63, 65); **closest approach 0.0 A** — abuts the B7-1 surface.

### Spatial tiebreaker
| Site | B7-1 overlap | Closest approach | Verdict |
|------|--------------|------------------|---------|
| Guided (95-106) | 9 residues | 0.0 A | Direct steric block |
| Blind (61-70) | 2 residues | 0.0 A | Abuts B7-1 surface |

Both sites contact the B7-1 interface; neither is distant/allosteric.

---

## Limitations & Confidence

- **Restraint dependence:** the 95-106 mode is obtained with restraints directing the search toward the B7-1 region; it is *not* the global minimum of unguided scoring. The blind run localises nearby but not identically. The defensible claim is "ERY2-4 binds at the B7-1 interface", with the exact footprint unresolved.
- **No experimental reference structure:** no crystal structure of the ERY2-4/CTLA-4 complex exists, so CAPRI metrics reflect internal consistency, not accuracy against ground truth.
- **Single peptide conformer:** one AlphaFold model was docked.
- **Determinism:** the guided workflow reproduces the same dominant solution across runs (stable/reproducible).

**Overall:** a well-supported, experimentally-consistent hypothesis for the ERY2-4 binding site — suitable for guiding confirmatory experiments, not a definitive structure.

---

## Suggested Next Steps

1. **Experimental discrimination (highest priority):** alanine mutagenesis to resolve the guided (95-106) vs blind (61-70) sites — e.g. CTLA-4 **Y104A / Y105A** or ERY2-4 **W34A** for the B7-competitive mode.
2. **Co-docking exclusivity test:** check whether ERY2-4 and B7-1 can occupy CTLA-4 simultaneously without clashing — mutual exclusivity supports the competitive model.
3. **Ensemble / enhanced sampling:** dock multiple AlphaFold conformers; increase blind sampling to test whether the B7 site appears among lower-ranked unguided clusters.

---

## References

1. Ramanayake, S. et al. *Affinity Maturation of Helix-Loop-Helix Peptides that Target CTLA-4.* ACS Chem. Biol. 2020, 15, 360-368.
2. HADDOCK3 — BonvinLab. https://github.com/haddocking/haddock3
3. AlphaFold2 / ColabFold — Mirdita, M. et al. Nat. Methods 2022.
4. PDB 1I8L — Structure of the CTLA-4/B7-1 complex.

---

*This repository contains a computational prediction intended for research and supervisory review. It is not an experimentally-determined structure.*
