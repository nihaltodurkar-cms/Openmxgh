#!/usr/bin/env python3
"""
One-page PDF summary of the effective-mass analysis for MoS2 4x4 + 2 S vacancies.
Revision 4: 2D k-grids at both extrema (mesh2d/) give the full mass tensors.
Revision 3: fine k-mesh run near K_sc (fine_k/) resolves the electron mass.
Revision 2: corrections following referee review.

  - vacancy separation corrected 3.6 -> 6.32 A (the 3.6 figure was a Mo-vacancy
    distance); "non-interacting" removed and replaced by a quantified coupling
    statement
  - defect manifold: "total width 37 meV" corrected to 138 meV spread /
    50 meV largest single-band dispersion; upper level +0.635 -> +0.663 eV
  - electron mass: no value reported (was an unsupported 0.4-0.55 range)
  - defect row: crystal momentum and "m* -> inf" both removed
  - band edges drawn as dispersion bands, not flat lines
"""
import cairo

W, H = 595.28, 841.89          # A4
ML, MR = 46, 46

INK = (0.09, 0.10, 0.12)
MUTED = (0.42, 0.45, 0.50)
RULE = (0.78, 0.80, 0.84)
ACC = (0.72, 0.24, 0.12)
OKC = (0.13, 0.42, 0.24)
BLU = (0.20, 0.34, 0.60)
GRY = (0.48, 0.52, 0.58)

surf = cairo.PDFSurface("effective_mass_MoS2_2V.pdf", W, H)
cr = cairo.Context(surf)
surf.set_metadata(cairo.PDF_METADATA_TITLE,
                  "Effective masses - MoS2 4x4 monolayer with two S vacancies")
surf.set_metadata(cairo.PDF_METADATA_CREATOR, "OpenMX 4.0 post-analysis")

SANS, MONO = "DejaVu Sans", "DejaVu Sans Mono"


def font(name=SANS, size=9, bold=False):
    cr.select_font_face(name, cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)


def txt(x, y, s, col=INK):
    cr.set_source_rgb(*col)
    cr.move_to(x, y)
    cr.show_text(s)


def rtxt(x, y, s, col=INK):
    cr.set_source_rgb(*col)
    cr.move_to(x - cr.text_extents(s).x_advance, y)
    cr.show_text(s)


def rule(y, x0=ML, x1=W - MR, col=RULE, w=0.6):
    cr.set_source_rgb(*col)
    cr.set_line_width(w)
    cr.move_to(x0, y)
    cr.line_to(x1, y)
    cr.stroke()


def band(y, h, col=(0.93, 0.94, 0.96)):
    cr.set_source_rgb(*col)
    cr.rectangle(ML, y, W - MR - ML, h)
    cr.fill()


y = 56
font(SANS, 15, bold=True)
txt(ML, y, "Effective Masses")
y += 16
font(SANS, 10.5)
txt(ML, y, "MoS₂ 4×4 monolayer with two sulfur vacancies", MUTED)
y += 12
font(SANS, 8)
txt(ML, y, "OpenMX 4.0  ·  GGA-PBE  ·  spin-polarized  ·  46 atoms (16 Mo, 30 S)", MUTED)
y += 7
rule(y)

# ------------------------------------------------------------- system
y += 15
font(SANS, 9.3, bold=True)
txt(ML, y, "System and reference levels")
y += 12
rows = [
    ("Vacancies", "two S vacancies, one per sulfur layer; separation 6.32 Å"),
    ("", "(3.19 Å in-plane, 3.12 Å across); nearest image 12.76 Å"),
    ("Symmetry", "neither C₃ nor σ_h retained (verified on the relaxed structure)"),
    ("Relaxation", "|F|max = 3.22e-4 Ha/Bohr (criterion 5.0e-4), converged at MD = 23"),
    ("Magnetism", "spin-polarized calculation converged to zero moment (0.000 μB)"),
    ("Fermi level", "E_F = -5.239 eV, OpenMX absolute scale (not vacuum-aligned);"),
    ("", "pinned only to within the gap at 789.5 K smearing"),
    ("VBM", "band 202, at Γ, -0.471 eV rel. E_F  (band dispersion 79 meV)"),
    ("Host CB edge", "band 207, +1.167 eV; min lies 0.0031 Bohr⁻¹ off K_sc along Γ-K"),
    ("", "(0.22 meV below E(K_sc)); K_sc is not a symmetry-protected extremum"),
    ("Defect levels", "bands 203-206, +0.525 to +0.663 eV; manifold spread 138 meV,"),
    ("", "largest single-band dispersion 50 meV (band 204)"),
]
for k, v in rows:
    if k:
        font(MONO, 7.6, bold=True)
        txt(ML + 4, y, k)
    font(MONO, 7.6)
    txt(ML + 92, y, v)
    y += 10.2

# ------------------------------------------------------------- method
y += 6
font(SANS, 9.3, bold=True)
txt(ML, y, "Method")
y += 12
font(MONO, 7.6)
for l in [
    "Atomic units throughout (ħ = m_e = 1), so the mass tensor is the inverse Hessian of E(k).",
    "SCF: 6×6×1 mesh, scf.criterion 1e-8, restarted from the relaxed density.",
    "C₃ breaking makes K_sc a non-symmetry point, so a linear term in E(k) is allowed",
    "there and is present; at Γ it vanishes, as time-reversal requires.",
    "Masses come from 2D grids at both extrema: 21×21 points, ±0.008 Bohr⁻¹ on orthogonal",
    "cartesian axes, spacing 8e-4 (mesh2d/, 882 k-points, 896 s). Fitting",
    "E = E0 + p·k + ½ k·H·k gives the mass tensor M = H⁻¹; principal masses are 1/eig(H).",
]:
    txt(ML + 4, y, l)
    y += 10.2

# ------------------------------------------------------------- results
y += 7
font(SANS, 9.3, bold=True)
txt(ML, y, "Results")
y += 5
band(y, 14)
y += 10
font(MONO, 7.6, bold=True)
txt(ML + 4, y, "carrier")
txt(ML + 54, y, "band")
txt(ML + 108, y, "extremum")
rtxt(ML + 292, y, "m1")
rtxt(ML + 340, y, "m2")
rtxt(ML + 396, y, "m_DOS")
rtxt(ML + 446, y, "axis")
y += 5
rule(y, w=0.5)
y += 11
res = [
    ("hole", "202", "Γ (exact)", "-2.273", "-1.975", "2.119", "61.6°", INK),
    ("electron", "207", "0.0031 Bohr⁻¹ off K_sc (Γ-K)", "+0.591", "+0.620", "0.606", "60.6°", INK),
    ("defect", "203-206", "not defined (localized state)", "—", "—", "—", "—", ACC),
]
font(MONO, 7.6)
for c0, c1, c2, m1, m2, md, ax, col in res:
    txt(ML + 4, y, c0)
    txt(ML + 54, y, c1)
    txt(ML + 108, y, c2, col)
    rtxt(ML + 292, y, m1, col)
    rtxt(ML + 340, y, m2, col)
    rtxt(ML + 396, y, md, col)
    rtxt(ML + 446, y, ax, col)
    y += 10.4
rule(y - 3, w=0.5)

y += 11
font(SANS, 8.2, bold=True)
txt(ML, y, "Summary:  principal masses (m1, m2) and their geometric mean m_DOS, in units of m_e;")
y += 10
txt(ML, y, "axis = principal-axis angle from cartesian x. Hole anisotropy 15%, electron 5%.")

# ------------------------------------------------------------- convergence
y += 16
font(SANS, 9.3, bold=True)
txt(ML, y, "Convergence of the mass tensors against fit radius")
y += 11
font(SANS, 7.6)
txt(ML + 4, y, "Quadratic fitted to all grid points within the given radius of the extremum.", MUTED)
y += 5
band(y, 13)
y += 9.5
font(MONO, 7.6, bold=True)
txt(ML + 4, y, "radius (Bohr⁻¹)")
for i, n in enumerate(("0.003", "0.004", "0.005", "0.006", "0.008")):
    rtxt(ML + 168 + i * 62, y, n)
y += 5
rule(y, w=0.5)
y += 11
font(MONO, 7.6)
for lab, vals in [
    ("electron  m1", ["0.5900", "0.5899", "0.5902", "0.5904", "0.5908"]),
    ("electron  m2", ["0.6197", "0.6205", "0.6200", "0.6201", "0.6205"]),
    ("hole      m1", ["-2.2726", "-2.2726", "-2.2726", "-2.2726", "-2.2727"]),
    ("hole      m2", ["-1.9732", "-1.9734", "-1.9737", "-1.9740", "-1.9748"]),
    ("rms resid. (meV)", ["0.0002", "0.0006", "0.0012", "0.0020", "0.0047"]),
]:
    txt(ML + 4, y, lab)
    for i, v in enumerate(vals):
        rtxt(ML + 168 + i * 62, y, v)
    y += 10.4
rule(y - 3, w=0.5)

y += 11
font(SANS, 7.7)
for l in [
    "All four principal masses are stable to <0.2% over a 2.7× change in radius; principal axes move by <0.1°. The fitted",
    "conduction extremum sits 0.00306 Bohr⁻¹ from K_sc at 59.7°, i.e. on the Γ-K axis, independently reproducing the 1D scan.",
    "Two-line sampling had understated the hole anisotropy as 4% against the true 15%: two directions cannot fix a symmetric",
    "2×2 tensor, which has three independent components. The earlier line values (0.590, 0.612) bracket the electron tensor well.",
]:
    txt(ML + 4, y, l)
    y += 9.6

# ------------------------------------------------------------- caveats
y += 8
font(SANS, 9.3, bold=True)
txt(ML, y, "Caveats")
y += 11
font(SANS, 7.7)
cav = [
    ("1.", "These are defective-supercell masses, not pristine MoS₂. The valence edge carries 3.7× enhanced vacancy character",
     "(per-atom PDOS over -0.52 to -0.42 eV, against a Mo 6.63 Å from either vacancy), so the hole tensor is partly perturbed."),
    ("2.", "The VBM sits at Γ, not at the zone corner, because of 4×4 zone folding. This is a Γ-valley hole mass and is not",
     "comparable to the commonly quoted K-valley hole mass of pristine monolayer MoS₂."),
    ("3.", "No effective mass is defined for bands 203-206: effective-mass theory presupposes a slowly-varying envelope over a",
     "delocalized Bloch band, which deep localized levels violate. Their residual dispersion is a finite-size artifact."),
    ("4.", "Sixteen primitive k-points fold onto each supercell k-point; the bands were not unfolded, so the primitive-cell origin",
     "of bands 202 and 207 is not established, and no pristine 4×4 reference was computed."),
    ("5.", "Masses are the quadratic term of a fit over ±0.008 Bohr⁻¹; they describe carriers within a few meV of the band edges",
     "and should not be extrapolated to higher energies, where the bands are measurably non-parabolic."),
]
for n, l1, l2 in cav:
    font(SANS, 7.7, bold=True)
    txt(ML + 4, y, n)
    font(SANS, 7.7)
    txt(ML + 16, y, l1)
    y += 9.2
    txt(ML + 16, y, l2)
    y += 8.8

# ------------------------------------------------------------- level map
y += 2
font(SANS, 9.3, bold=True)
txt(ML, y, "Band-edge map  (eV relative to E_F)")
y += 9

BX, BW, BH = ML + 4, 250, 86
BY = y
E_LO, E_HI = -0.95, 1.62
X0, X1 = BX + 40, BX + 150


def lv(e):
    return BY + BH - (e - E_LO) / (E_HI - E_LO) * BH


cr.set_source_rgb(0.99, 0.99, 1.0)
cr.rectangle(BX, BY, BW, BH)
cr.fill()
cr.set_source_rgb(*RULE)
cr.set_line_width(0.6)
cr.rectangle(BX, BY, BW, BH)
cr.stroke()

# E_F
cr.set_source_rgb(0.2, 0.2, 0.2)
cr.set_line_width(0.8)
cr.set_dash([3, 2])
cr.move_to(BX, lv(0))
cr.line_to(BX + BW, lv(0))
cr.stroke()
cr.set_dash([])
font(SANS, 6.6, bold=True)
txt(BX + BW - 22, lv(0) - 2.5, "E_F", (0.2, 0.2, 0.2))


def dispband(e0, e1, col, fill):
    """Draw a band edge as a box spanning its actual dispersion."""
    cr.set_source_rgb(*col)
    if fill:
        cr.rectangle(X0, lv(e1), X1 - X0, lv(e0) - lv(e1))
        cr.fill()
    else:
        cr.set_line_width(0.9)
        cr.rectangle(X0, lv(e1), X1 - X0, lv(e0) - lv(e1))
        cr.stroke()


# host CB edge (empty) 1.167 -> 1.501
dispband(1.1674, 1.5007, GRY, False)
font(SANS, 6.8)
txt(X1 + 6, lv(1.30) + 2, "host CB edge  +1.167", MUTED)
font(SANS, 6.2)
txt(X1 + 6, lv(1.30) + 9, "min 0.0031 Bohr⁻¹ off K_sc", MUTED)
font(SANS, 6.8)

# defect levels (empty), each with its own dispersion
for e0, e1 in ((0.5250, 0.5624), (0.5604, 0.6105), (0.6050, 0.6338), (0.6349, 0.6633)):
    dispband(e0, e1, ACC, False)
font(SANS, 6.8, bold=True)
txt(X1 + 6, lv(0.62) - 1, "4 defect levels", ACC)
font(SANS, 6.8)
txt(X1 + 6, lv(0.62) + 7, "+0.525 .. +0.663", ACC)

# VBM (occupied) -0.550 -> -0.471
dispband(-0.5504, -0.4712, BLU, True)
font(SANS, 6.8)
txt(X1 + 6, lv(-0.51) + 2, "VBM (Γ)  -0.471", BLU)

# separations
cr.set_source_rgb(0.35, 0.37, 0.40)
cr.set_line_width(0.6)
for e0, e1, xo in ((-0.4712, 0.5250, 26), (-0.4712, 1.1674, 13)):
    cr.move_to(BX + xo, lv(e0))
    cr.line_to(BX + xo, lv(e1))
    cr.stroke()
font(SANS, 6.0)
for xo, ymid, lab in ((24, lv(-0.30), "0.996 eV"),
                      (11, lv(-0.30), "1.638 eV")):
    cr.save()
    cr.translate(BX + xo, ymid)
    cr.rotate(-1.5708)
    cr.move_to(0, 0)
    cr.set_source_rgb(0.35, 0.37, 0.40)
    cr.show_text(lab)
    cr.restore()

font(SANS, 6.2)
txt(BX + 4, BY + BH - 5, "filled box = occupied · open box = empty · box height = band dispersion", MUTED)

# side notes
nx = BX + BW + 14
ny = BY + 12
font(SANS, 8, bold=True)
txt(nx, ny, "Reading the masses off this map")
ny += 11.5
font(SANS, 7.0)
for l in ["Hole mass = curvature of the VBM box at Γ.",
          "Electron mass = curvature of the host CB edge,",
          "whose minimum lies just off K_sc — hence the",
          "linear term in the fit.",
          "Defect levels show their true dispersion; that",
          "width is defect-image coupling, not transport.",
          "Vertical bars: 0.996 eV = VBM → lowest defect",
          "level, 1.638 eV = VBM → host CB edge.",
          "Neither is a band gap."]:
    txt(nx, ny, l, MUTED if l else INK)
    ny += 7.2

# ------------------------------------------------------------- footer
rule(H - 44)
font(SANS, 6.8)
txt(ML, H - 33, "Sources: props/test_1.Band (Γ-M-K_sc-Γ overview), fine_k/test_1.Band (1D scans through K_sc), "
                "mesh2d/test_1.Band (2D tensors).", MUTED)
txt(ML, H - 24, "Mass tensors from two 21×21 grids (±0.008 Bohr⁻¹, spacing 8e-4) centred on Γ and on K_sc; "
                "882 k-points, 896 s wall.", MUTED)

cr.show_page()
surf.finish()
print("wrote effective_mass_MoS2_2V.pdf")
