# fastsolv GitHub Action

Automatically predicts **solid solubility (logS)** for a list of solute–solvent–temperature combinations using the [fastsolv](https://github.com/JacksonBurns/fastsolv) model. Results are uploaded as a downloadable CSV artifact.

---

## How It Works

```
input.csv  →  GitHub Actions  →  fastsolv model  →  predictions.csv (artifact)
```

The workflow installs `fastsolv`, runs inference on your input CSV, and uploads a `predictions.csv` you can download directly from the Actions tab.

---

## Input Format

Your CSV must contain these three columns (tab- or comma-separated):

| Column | Description |
|---|---|
| `solvent_smiles` | SMILES string of the solvent |
| `solute_smiles` | SMILES string of the solute |
| `temperature` | Temperature in Kelvin (e.g. `298.15`) |

**Example (`input.csv`):**
```
solvent_smiles	solute_smiles	temperature
CC(=O)C	CC(C=C1)=CC2=C1C(C)(C)OC3=C2C(O)=CC(C(O)CCCC)=C3	298.15
CC#N	CC(C=C1)=CC2=C1C(C)(C)OC3=C2C(O)=CC(C(O)CCCC)=C3	298.15
```

---

## Output Format

The artifact `predictions.csv` contains all input columns plus:

| Column | Description |
|---|---|
| `logS` | Predicted log solubility (ensemble mean across 4 models) |
| `logS_stdev` | Standard deviation across ensemble (uncertainty estimate) |

---

## Usage

### Option A — Push to trigger automatically

1. Edit `input.csv` with your data
2. Commit and push — the workflow runs automatically

```bash
git add input.csv
git commit -m "Update input data"
git push
```

### Option B — Trigger manually (with a custom CSV file)

1. Push your CSV file to the repository (e.g. `inputs/my_compounds.csv`)
2. Go to **Actions → FastSolv Solubility Prediction → Run workflow**
3. Enter the path to your file (e.g. `inputs/my_compounds.csv`)
4. Click **Run workflow**

### Downloading Results

1. Go to **Actions** tab → click your completed workflow run
2. Scroll to the **Artifacts** section at the bottom
3. Click **fastsolv-predictions** to download `predictions.csv`

---

## Workflow Details

- **Runner:** `ubuntu-latest`
- **Python:** 3.11
- **Model:** fastsolv ensemble of 4 models (checkpoints from [Zenodo](https://zenodo.org/records/13943074))
- **Caching:** pip packages and model checkpoints are cached — after the first run, subsequent runs skip the ~500 MB checkpoint download
- **Artifact retention:** 30 days

---

## Reference

> Attia, Burns, Doyle, Green — *"Solid Solubility Prediction at the Limit of Aleatoric Uncertainty"*
> 
> fastsolv package: https://github.com/JacksonBurns/fastsolv
