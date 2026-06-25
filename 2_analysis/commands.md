# Reproducible assembly commands

```bash
python 2_analysis/scripts/assemble_controlled_validation_composite.py   --ab 1_experiment/source_artwork/fig4_ab_protocol_tapestation_src.pdf   --tapestation 1_experiment/source_artwork/fig4_tapestation.png   --panelC 1_experiment/source_artwork/panel_c_fig3_real_distributions.pdf   --out 3_results/figures/figure4_controlled_validation_composite.pdf

pdftocairo -png -singlefile 3_results/figures/figure4_controlled_validation_composite.pdf 3_results/figures/figure4_controlled_validation_composite
pdftocairo -svg 3_results/figures/figure4_controlled_validation_composite.pdf 3_results/figures/figure4_controlled_validation_composite.svg
```
