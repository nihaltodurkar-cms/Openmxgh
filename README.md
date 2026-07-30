# Sulfur-Vacancy Defect States in Monolayer MoS₂

First-principles study of a double sulfur-vacancy defect in a 4×4 supercell of
monolayer MoS₂, computed with the linear-combination-of-pseudo-atomic-orbitals
(LCAO) DFT code [OpenMX](http://www.openmx-square.org/) 4.0. The repository
contains the full input/output chain — structure relaxation, ground-state SCF,
band structure, tetrahedron DOS/PDOS, Fermi surfaces, and quadratic k·p fits
of the valence/conduction effective-mass tensors — together with the scripts
used to turn the raw OpenMX output into the figures and the results summary
below.

![Bands and DOS](props/bands_dos.svg)

*Band structure (Γ–M–K–Γ) and total/projected DOS around the gap. The four
sulfur-vacancy defect levels (red) sit inside the host gap; the dashed blue
curve is the PDOS of a Mo atom 6.6 Å from either vacancy, scaled ×6, shown as
an unperturbed reference.*

## System

- **Structure**: 4×4 supercell of monolayer 2H-MoS₂, hexagonal cell
  *a* = *b* = 12.7613 Å, γ = 120°, 15 Å vacuum along *c* (2D slab).
- **Composition**: 46 atoms — 16 Mo, 30 S (stoichiometric would be 32 S).
  Two sulfur vacancies are introduced, one in each S sublayer (top and
  bottom), separated by 6.32 Å (3.19 Å in-plane, 3.12 Å across the layer).
  Periodic images are 12.76 Å apart, i.e. one full lattice vector.
- **Starting geometry**: derived from the experimental 2H-MoS₂ structure
  ([`test_1.cif`](test_1.cif), Materials Studio, *P*1) with the two S atoms
  removed and coordinates converted to Cartesian ([`input.dat`](input.dat)).

## Method

| | |
|---|---|
| Code | OpenMX 4.0 |
| Exchange-correlation | GGA-PBE |
| Basis (PAO) | Mo7.0-s3p2d2 (3s2p2d, 7.0 a₀ cutoff), S7.0-s2p2d1f1 (2s2p1d1f, 7.0 a₀ cutoff) |
| Pseudopotentials | Mo_PBE19, S_PBE19 (norm-conserving, `DFT_DATA19` set) |
| Real-space grid cutoff | 200 Ry |
| Spin treatment | spin-polarized (collinear) |
| Electronic smearing | 789.5 K (0.068 eV) |
| SCF k-mesh | 6×6×1 Monkhorst–Pack |
| SCF mixing | RMM-DIIS(k), history 30, Pulay restart at 15 |
| SCF convergence | ΔE < 1×10⁻⁸ Ha |
| Geometry optimization | BFGS, force criterion 5×10⁻⁴ Ha/Bohr |

## Repository layout

The four directories mirror the actual calculation pipeline, in the order
they were run:

```
.
├── input.dat, test_1.{cif,xyz,bulk.xyz}   structure + relaxation setup
├── test_1.{out,ene,md,md2}                relaxation / ground-state SCF output
│
├── fine_k/       1D band scan straddling the (displaced) supercell K-point,
│                 to locate the true conduction-band minimum
├── props/        Γ–M–K–Γ band overview, tetrahedron DOS/PDOS, Fermi surfaces,
│                 and the two post-processing scripts + their output figures
└── mesh2d/       21×21 2D k-grids centred on Γ and on K_sc, used to fit the
                  full valence/conduction effective-mass tensors
```

Each subdirectory's `input.dat` is a single-point (`MD.Type NOMD`) restart
from the relaxed, converged density (`scf.restart on`) — SCF parameters are
kept identical to the relaxation run, as required for the restart density to
be valid; this is called out explicitly in comments inside those files.

Large, fully regenerable OpenMX output — volumetric `.cube` files (charge,
spin, Hartree potential; ~15 MB each), binary restart directories
(`test_1_rst/`), and the raw DOS eigenvector dump (`test_1.Dos.vec`,
~200 MB) — is intentionally **not** tracked here; see
[Reproducing the calculations](#reproducing-the-calculations).

## Results

### Energetics and relaxation

- Final total energy: **−1437.505660081 Ha** (−39116.52 eV).
- BFGS relaxation converged at MD step 23, |F|<sub>max</sub> = 3.22×10⁻⁴
  Ha/Bohr (criterion 5×10⁻⁴).
- Neither the C₃ rotation nor the σ<sub>h</sub> mirror of the pristine lattice
  survives in the relaxed, defected structure.

### Magnetism

The spin-polarized SCF converges to a **zero net magnetic moment**
(Mulliken populations: 202.00000 up / 202.00000 down) — the two-vacancy
defect does not carry a spin moment in this configuration.

### Electronic structure

Energies below are relative to E_F = −5.239 eV (OpenMX's internal absolute
scale; not aligned to vacuum).

| Feature | Band(s) | Energy (eV) | Notes |
|---|---|---|---|
| VBM | 202 | −0.471 | at Γ (exact); 79 meV dispersion |
| Defect manifold | 203–206 | +0.525 … +0.663 | 138 meV total spread, localized S-vacancy states |
| Host CB edge | 207 | +1.167 | minimum 0.0031 Bohr⁻¹ off the supercell K-point along Γ–K |

VBM → lowest defect level: **0.996 eV**. VBM → host conduction band:
**1.638 eV**. Neither is "the" band gap in the usual sense, since the defect
levels sit inside it.

The host conduction-band minimum is displaced slightly off the supercell
K-point (K<sub>sc</sub>) because the two vacancies break the 3-fold symmetry
that would otherwise pin it there — `fine_k/` was run specifically to locate
this displaced minimum before the 2D mass-tensor fits in `mesh2d/`.

### Effective masses

Fitted from 21×21 2D k-grids (±0.008 Bohr⁻¹, 8×10⁻⁴ Bohr⁻¹ spacing,
882 k-points, `mesh2d/`) to *E* = *E*₀ + **p**·**k** + ½ **k**·*H*·**k**;
principal masses are the eigenvalues of *H*⁻¹. Stable to <0.2% over a 2.7×
change in fit radius (see [`props/effective_mass_MoS2_2V.pdf`](props/effective_mass_MoS2_2V.pdf)
for the full convergence table and derivation).

| Carrier | Band | Extremum | m₁ | m₂ | m<sub>DOS</sub> | Axis |
|---|---|---|---|---|---|---|
| Hole | 202 | Γ (exact) | −2.273 | −1.975 | 2.119 | 61.6° |
| Electron | 207 | 0.0031 Bohr⁻¹ off K<sub>sc</sub> (Γ–K) | +0.591 | +0.620 | 0.606 | 60.6° |
| Defect | 203–206 | not defined | — | — | — | localized; effective-mass theory does not apply |

All masses in units of *m*ₑ. Hole-mass anisotropy 15%, electron-mass
anisotropy 5%.

**Caveats** (full discussion in [`props/effective_mass_MoS2_2V.pdf`](props/effective_mass_MoS2_2V.pdf)):
these are defective-supercell masses, not pristine-MoS₂ masses; the VBM sits
at Γ rather than the zone corner because of 4×4 zone folding, so it is not
directly comparable to the commonly quoted K-valley hole mass of pristine
monolayer MoS₂; bands were not unfolded; and the defect-band dispersion is a
finite-size (image-coupling) artifact rather than a transport property.

## Reproducing the calculations

You will need:

1. **OpenMX 4.0** built with MPI (see [openmx-square.org](http://www.openmx-square.org/)
   for source and build instructions), and the `DFT_DATA19` pseudopotential /
   PAO basis-set archive.
2. Edit `DATA.PATH` at the top of each `input.dat` to point at your local
   `DFT_DATA19` directory, and `System.CurrrentDirectory` to the directory
   you're running in (OpenMX writes its output relative to this path).

Then, in order:

```bash
# 1. relax the defected structure + ground-state SCF (root input.dat)
mpirun -np <N> openmx input.dat

# 2. copy the converged density/geometry into fine_k/, props/, mesh2d/
#    (each subdirectory's input.dat already has the relaxed coordinates
#    baked in; you just need the restart density alongside it)
mpirun -np <N> openmx fine_k/input.dat
mpirun -np <N> openmx props/input.dat
mpirun -np <N> openmx mesh2d/input.dat

# 3. regenerate the figure and the effective-mass summary
cd props
python3 plot_bands_dos.py        # -> bands_dos.svg
python3 make_effmass_pdf.py      # -> effective_mass_MoS2_2V.pdf  (needs pycairo)
```

The main relaxation run took ≈4.3 h wall time on 5 MPI ranks; the `mesh2d/`
2D-grid run (882 k-points) took ≈15 min.

`plot_bands_dos.py` is pure standard-library Python (writes SVG directly).
`make_effmass_pdf.py` additionally requires [`pycairo`](https://pycairographics.readthedocs.io/).

## License

Code and data in this repository are released under the [MIT license](LICENSE).

## Citing

See [`CITATION.cff`](CITATION.cff). If you use OpenMX itself, please also
cite it per the policy on the [OpenMX website](http://www.openmx-square.org/);
the PAO/pseudopotential method is described in Ozaki, *Phys. Rev. B* **67**,
155108 (2003) and Ozaki & Kino, *Phys. Rev. B* **69**, 195113 (2004).
