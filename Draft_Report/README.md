# Draft report: Noise-Aware Spectrally Adaptive Wiener Deconvolution

First full draft, written 30 Oct from the results that existed in `DSP_Deconv/results/` on that date. **Nothing in the notebooks has been re-run since**, so several numbers are placeholders or preliminary.

## Files (one per section, owner in brackets)

| File | Section | Owner |
|---|---|---|
| `00_abstract.md` | Abstract | P3 |
| `01_introduction.md` | 1 Introduction | P3 |
| `02_forward_model.md` | 2 Forward imaging model | P1 |
| `03_regularized_inverse.md` | 3 Regularized inverse derivation | P3 |
| `04_proposed_method.md` | 4 Proposed method | P3 |
| `05_baselines.md` | 5 Baselines and implementation | P2 |
| `06_experimental_setup.md` | 6 Experimental setup | P1 |
| `07_results_synthetic.md` | 7 Results on the controlled benchmark | P2 |
| `08_ablation.md` | 8 Ablation | P3 |
| `09_robustness.md` | 9 Robustness | P2 |
| `10_real_images.md` | 10 Real biomedical images | P1 |
| `11_discussion_limitations.md` | 11 Discussion and limitations | P3 (all) |
| `12_conclusion.md` | 12 Conclusion | P3 |
| `references.md` | References | all |
| `appendix_reproducibility.md` | Appendix: how to reproduce | P1 |

## Markers used in the text

- **[TBD: …]** a number or figure that does not exist yet. It names the notebook cell that produces it.
- **[PRELIM: …]** a number from a test run on a laptop against the Drive snapshot (newer numpy/scikit-image than Colab). Replace it with the Colab value before submission.
- **[CHECK: …]** a claim a teammate should verify (a citation detail or an assumption).
- Numbers with no marker come from CSVs or notebook outputs already on Drive (Colab runs of 29–30 Oct).

## Before submitting

1. Re-run in this order: 01 (`metrics.py` cell, `[S3 tuning]`, `[S3 check]`) → 03 (Run all) → 02 (Ablation cells) → 04 (Run all) → 05 (Run all).
2. Re-tuning RL changes `tuned.yaml`. Every number for `wiener_const` and `rl` in Section 7 must then be refreshed from `results/tables/table1_gauss_psnr.csv`. The proposed method, Tikhonov-GCV and the oracle do not use `tuned.yaml`, so their numbers will not change.
3. Replace every **[TBD]**/**[PRELIM]**, and resolve every **[CHECK]**.
4. Check the course's rules on AI assistance and add an acknowledgement if required. This draft and parts of the code were prepared with help from Claude (Anthropic).
5. Merge the sections into one document (Word/LaTeX/Docs), number the figures and tables, and make sure every figure is cited in the text.
