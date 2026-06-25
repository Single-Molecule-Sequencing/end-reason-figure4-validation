# HAPPY PATH — Figure 4 controlled-validation composite

## 1) Environment
```bash
conda env create -f 2_analysis/environment.yaml -n end-reason-fig4 || true
conda activate end-reason-fig4
```

## 2) Assemble composite (A/B/C)
```bash
python 2_analysis/scripts/assemble_controlled_validation_composite.py   --ab 1_experiment/source_artwork/fig4_ab_protocol_tapestation_src.pdf   --tapestation 1_experiment/source_artwork/fig4_tapestation.png   --panelC 1_experiment/source_artwork/panel_c_fig3_real_distributions.pdf   --out 3_results/figures/figure4_controlled_validation_composite.pdf
```

## 3) Export PNG + SVG
```bash
pdftocairo -png -singlefile 3_results/figures/figure4_controlled_validation_composite.pdf 3_results/figures/figure4_controlled_validation_composite
pdftocairo -svg 3_results/figures/figure4_controlled_validation_composite.pdf 3_results/figures/figure4_controlled_validation_composite.svg
```

## 4) Verify checksums
Compare with `provenance/artifact_checksums.txt`.
