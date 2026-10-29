# Appendix A: How to reproduce

**Environment.** Google Colab, CPU runtime, with the shared Google Drive folder `DSP_Deconv` mounted at `/content/drive/MyDrive/DSP_Deconv`. Every notebook starts with the same four setup cells: mount, paths, packages, config. Package versions are in `results/versions.txt`.

**Folder layout**
```
DSP_Deconv/
  lib/        forward.py  data.py  metrics.py  baselines.py  proposed.py
  configs/    params.yaml (grids, seeds)  tuned.yaml (dev-tuned NSR, RL iterations)  split.yaml (dev/test)
  data/raw/   FMD/<subset>/{raw,gt}/<fov>/*.png    OCT/*.jpeg
  results/    *.csv   tables/*.csv   versions.txt
  figures/    *.png
```

**Run order (about 20–30 min of compute in total)** [CHECK: timing after the first full run]

| Notebook | Cells | Produces |
|---|---|---|
| 00_setup_data | all | downloads FMD subsets and the OCT sample |
| 01_forward_baselines | all | writes the five `lib/` files; `tuned.yaml` |
| 03_experiments | all | `synthetic_gauss_test.csv`, `synthetic_pg_test.csv`, `edge_test.csv`, `wilcoxon.csv`, `psf_mismatch.csv`, `boundary.csv` |
| 02_proposed | all | `ablation.csv` |
| 04_real_data | all | `split.yaml`, `versions.txt`, `real_fmd.csv`, `real_oct.csv`, real-data figures |
| 05_figures | all | `fig1`–`fig7`, `results/tables/table*.csv` |

**Ownership of library files.** Each `lib/*.py` file is written by a `%%writefile` cell, and that cell is the source of truth:
- `forward.py`, `data.py`, `metrics.py` are written by 01 (owner P1);
- `baselines.py` by 01 (owner P2);
- `proposed.py` by 02 (owner P3).

Editing a `.py` file directly on Drive is overwritten the next time its cell runs.

**Determinism.** All noise is drawn with `numpy.random.default_rng(seed)`, seeds 0–4. Re-running 03 on a fresh runtime reproduces the CSVs exactly, as long as the package versions match. `unsupervised_wiener` uses its own sampler, so its outputs vary slightly from run to run.

**Do not run `test.ipynb`.** It overwrites `lib/forward.py` with a stub. Delete it before submission.
