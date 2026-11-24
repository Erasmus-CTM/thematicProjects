# RUB Tutorials

Interactive Quarto tutorials from Ruhr-Universität Bochum (RUB), written for the CTM project. Students run Python in the browser, solve exercises that are checked automatically and get AI feedback; nothing needs to be installed on their computers.

| Tutorial | Topic | Languages |
|---|---|---|
| [Kurvendiskussion](Kurvendiskussion/) | Curve sketching: domain, symmetry, asymptotes, monotonicity, curvature, graphs | German, English |
| [Matrizen](Matrizen/) | Vectors and matrices with NumPy: operations, transformations, linear systems, eigenvalues | German, English |
| [Statistik](Statistik/) | Descriptive statistics, estimation, significance and p-values | German, English |
| [Quarto Tutorial](Quarto-Tutorial/) | How to build such material yourself with Quarto, from a first page to interactive exercises | German, English, Swedish, Norwegian, Danish |

Each folder holds the complete source and the rendered site in `docs/`. Open `docs/index.html` through a local web server (for example `python -m http.server` inside `docs/`), not as a file: the Python cells need it.

## Building

- Quarto 1.8.27 or newer.
- The extensions are included in `_extensions/`. To update them, run in the tutorial's folder:
  - Windows: `quarto add https://erasmus-ctm.github.io/ctm-assessment/ctm-assessment.zip`
  - macOS / Linux: `quarto add https://erasmus-ctm.github.io/ctm-assessment/ctm-assessment.tar.gz`
- Render with the tutorial's build script (`build_multilingual_site.py --no-serve`, or `build.py --no-serve` for the Quarto Tutorial). It renders every language into `docs/`.

## Sources

The tutorials are maintained in their own repositories; this folder is a snapshot:

- Kurvendiskussion, Matrizen, Statistik: `gitlab.ruhr-uni-bochum.de/ctm/tutorials`
- Quarto Tutorial: [github.com/Erasmus-CTM/Quarto-Tutorial](https://github.com/Erasmus-CTM/Quarto-Tutorial)
