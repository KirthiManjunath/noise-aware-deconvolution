# Changes, 30 Oct (P1 + Claude)

**Nothing below has been run in Colab.** The edited cells have empty outputs. Upload the changed and new files to `DSP_Deconv/` on Drive, then run in the order at the bottom.

## Changed files

| File | Owner | Change |
|---|---|---|
| `lib/metrics.py` | P1 | `edge_metrics`: MTF50 now uses the **signed** line-spread function in a ±16 px window. The old `np.abs(np.diff(...))` turned noise into a positive floor, so MTF50 came out wrong (e.g. the oracle showed the sharpest edge but the lowest MTF50). FWHM, overshoot and noise columns were unaffected. |
| `01_forward_baselines.ipynb` | P1/P2 | Change-note cell at the top. The `metrics.py` `%%writefile` cell has the same fix (that cell is the source of truth; running it rewrites the file). `[S3 tuning]`: RL iteration grid now `[1, 2, 3, 4, 5, 7, 10, 20, 30, 50]` (the old best, 5, was the smallest value tried), and it warns when a best value is on a grid edge. **New `[S3 check]` cell**: compares the noise level estimated by `unsupervised_wiener` with the truth, to explain its poor scores. |
| `02_proposed.ipynb` | P3 | Change-note cell at the top. **Three new `[Ablation]` cells** at the end: full / oracle σ / oracle S_x / constant λ variants on the S6 test grid. Output: `results/ablation.csv`, a consistency check against S6, and a σ̂ and β accuracy table. |
| `03_experiments.ipynb` | P2 | Change-note cell at the top. **New `[S6 Cell B2]`**: Poisson–Gaussian grid, output `results/synthetic_pg_test.csv`. `[S6 Cell C]`: code unchanged, but must be re-run for correct MTF50. `[S6 Cell D]`: Wilcoxon tests for both noise models, now also win fraction and mean gain, output `results/wilcoxon.csv`. `[S7 Cell A]`: PSF mismatch over all 8 crops × 3 seeds, output `results/psf_mismatch.csv`. `[S7 Cell B]`: boundary test over 8 crops × 3 linear methods, output `results/boundary.csv` + `figures/boundary_error_map.png`. |

## New files

| File | Owner | What it is |
|---|---|---|
| `04_real_data.ipynb` | P1 | S8. Writes `configs/split.yaml` and `results/versions.txt`. Skips the 7 `._*` macOS junk files in `data/raw/OCT` (13 real B-scans remain). FMD real-noise test: filter designed once on the raw frame and applied to raw and avg50 → noise gain + chain MTF50, PSF σ ∈ {1, 1.5, 2}. OCT log-domain test. Outputs `real_fmd.csv`, `real_oct.csv` and three figures. |
| `05_figures.ipynb` | P3 | S9. Figures `fig1`–`fig7` and tables `results/tables/table1`–`table9` from the CSVs. Changes no results. |
| `Draft_Report/` | all | Full first draft, one Markdown file per section with the owner listed in `Draft_Report/README.md`. Markers: **[TBD]** = waiting on a run, **[PRELIM]** = number from a laptop test run, **[CHECK]** = verify. |
| `CHANGES.md` | — | This file. |

## Still to do by hand

1. **Delete `test.ipynb`.** Its last cell overwrites `lib/forward.py` with a "Hello" stub.
2. **Delete `results/Copy of synthetic_gauss_test.csv`.** It differs from the real CSV.
3. Re-tuning RL changes `tuned.yaml`, so every `wiener_const` / `rl` number must be refreshed afterwards.
4. Check the course's AI-assistance rules and add an acknowledgement if required.

## Run order

1. **01**: run all. This rewrites the lib files with the metrics fix, gives a new `tuned.yaml`, and runs the unsup-Wiener check.
2. **03**: run all (about 10 min).
3. **02**: run all, including the Ablation cells.
4. **04**: run all.
5. **05**: run all.
6. Fill the [TBD]/[PRELIM] markers in `Draft_Report/` from `results/tables/`.
