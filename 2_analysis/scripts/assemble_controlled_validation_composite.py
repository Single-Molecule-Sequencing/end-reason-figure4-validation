#!/usr/bin/env python
"""Assemble the Figure 4 controlled-validation three-panel composite.

Layout (clean, vector + one raster):
  Row A  Experimental protocol  -- clipped full-width from the end-reason-fresh
         composite; the stray duplicate "B" / "653-RC-9" / "Cut Regular 3040"
         labels that overlap the protocol's lower band are whited out.
  Row B  TapeStation electropherogram -- the standalone raster
         (source_artwork/fig4_tapestation.png, which already carries its
         "Cut Regular 3040" title + "A3: 13653-RC-9 used 2uL" sample note),
         placed CENTERED and large, with a fresh "B" panel label at the left
         margin so it lines up under the "A" label.
  Row C  End-reason-stratified read-length / Q-score distributions -- native
         from the figure-3 analysis repo.

Usage:
    python 2_analysis/scripts/assemble_controlled_validation_composite.py \
        --ab 1_experiment/source_artwork/fig4_ab_protocol_tapestation_src.pdf \
        --tapestation 1_experiment/source_artwork/fig4_tapestation.png \
        --panelC 1_experiment/source_artwork/panel_c_fig3_real_distributions.pdf \
        --out 3_results/figures/figure4_controlled_validation_composite.pdf
"""
from __future__ import annotations
import argparse
from pathlib import Path
import fitz

MARGIN = 8.0
GAP = 11.0
PAGE_W = 765.0
TS_W = 452.0           # TapeStation placed width (centred, large)
C_FRAC = 0.80          # Panel C width fraction (keeps figure+caption on one page)

# Source-coordinate regions in the A+B composite (points).
A_CLIP = fitz.Rect(24, 8, 360, 97)          # protocol + "A" label
# stray vector duplicates to erase from the protocol's lower band:
STRAYS = [
    fitz.Rect(80, 71, 122, 98),     # "B" box
    fitz.Rect(115, 74, 218, 96),    # "653-RC-9 used 2uL"
    fitz.Rect(255, 71, 360, 97),    # "Cut Regular 3040" (partial, to clip edge)
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ab", required=True, type=Path)
    ap.add_argument("--tapestation", required=True, type=Path)
    ap.add_argument("--panelC", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    ab = fitz.open(str(args.ab))
    pc = fitz.open(str(args.panelC))
    ts = fitz.open(str(args.tapestation))            # image -> get native AR
    ts_ar = ts[0].rect.height / ts[0].rect.width if ts.is_pdf else \
        fitz.Pixmap(str(args.tapestation)).height / fitz.Pixmap(str(args.tapestation)).width

    cw = PAGE_W - 2 * MARGIN
    scaleA = cw / A_CLIP.width
    hA = cw * (A_CLIP.height / A_CLIP.width)
    ts_h = TS_W * ts_ar
    cwid = cw * C_FRAC
    hC = pc[0].rect.height / pc[0].rect.width * cwid

    page_h = MARGIN + hA + GAP + ts_h + GAP + hC + MARGIN
    out = fitz.open()
    page = out.new_page(width=PAGE_W, height=page_h)

    # --- Row A: protocol, full width, strays erased ---
    yA = MARGIN
    page.show_pdf_page(fitz.Rect(MARGIN, yA, MARGIN + cw, yA + hA), ab, 0, clip=A_CLIP)
    for s in STRAYS:
        r = fitz.Rect(MARGIN + (s.x0 - A_CLIP.x0) * scaleA,
                      yA + (s.y0 - A_CLIP.y0) * scaleA,
                      MARGIN + (s.x1 - A_CLIP.x0) * scaleA,
                      yA + (s.y1 - A_CLIP.y0) * scaleA)
        page.draw_rect(r, color=None, fill=(1, 1, 1))

    # --- Row B: TapeStation raster centred + fresh "B" label at the margin ---
    yB = yA + hA + GAP
    tsx = MARGIN + (cw - TS_W) / 2
    page.insert_image(fitz.Rect(tsx, yB, tsx + TS_W, yB + ts_h),
                      filename=str(args.tapestation))
    # fresh "B" panel label, typeset to match the "A" box and aligned at the margin
    box = fitz.Rect(MARGIN, yB + 6, MARGIN + 55, yB + 61)
    try:
        page.draw_rect(box, color=(0, 0, 0), fill=(1, 1, 1), width=2.6, radius=0.16)
    except TypeError:
        page.draw_rect(box, color=(0, 0, 0), fill=(1, 1, 1), width=2.6)
    fs = 31
    tw = fitz.get_text_length("B", fontname="hebo", fontsize=fs)
    page.insert_text((box.x0 + (box.width - tw) / 2, box.y0 + box.height / 2 + fs * 0.36),
                     "B", fontname="hebo", fontsize=fs, color=(0, 0, 0))

    # --- Row C: distributions, near-full width ---
    yC = yB + ts_h + GAP
    cx = MARGIN + (cw - cwid) / 2
    page.show_pdf_page(fitz.Rect(cx, yC, cx + cwid, yC + hC), pc, 0)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.save(str(args.out), garbage=4, deflate=True)
    print(f"wrote {args.out}: {PAGE_W:.0f}x{page_h:.0f}pt AR={PAGE_W/page_h:.2f} "
          f"(TapeStation {TS_W:.0f}pt wide)")


if __name__ == "__main__":
    main()
