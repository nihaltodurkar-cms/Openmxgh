#!/usr/bin/env python3
"""
Standalone band-structure + DOS/PDOS plot for the MoS2 double-S-vacancy run.
Pure python, no numpy/matplotlib -- writes an SVG.

  python3 plot_bands_dos.py            -> bands_dos.svg
"""
import math

Ha = 27.2113845
EMIN, EMAX = -3.0, 3.0
NOCC = 202                      # 404 electrons / 2 spins
DEFECT = range(203, 207)        # 1-indexed defect bands
VAC_MO = [3, 6, 7, 8, 10, 11]   # Mo neighbouring the two S vacancies
CTRL_MO = 13                    # farthest Mo (6.63 A), unperturbed reference

# ---------------------------------------------------------------- geometry
W, H = 1120, 680
BX0, BX1 = 78, 690              # band panel
DX0, DX1 = 712, 1082            # dos panel
Y0, Y1 = 44, 600

C_HOST = "#98a2b3"
C_DEF = "#dc4b2a"
C_TOT = "#ccd3dd"
C_CTRL = "#2b7bba"
C_AX = "#33383f"


def ey(e):
    return Y1 - (e - EMIN) / (EMAX - EMIN) * (Y1 - Y0)


# ---------------------------------------------------------------- bands
def read_band(path="test_1.Band"):
    f = open(path).read().split("\n")
    nb, spin, chemp = int(f[0].split()[0]), int(f[0].split()[1]), float(f[0].split()[2])
    r = [float(x) for x in f[1].split()]
    b = [r[0:3], r[3:6], r[6:9]]
    npath = int(f[2].split()[0])
    i = 3
    segs = []
    for _ in range(npath):
        t = f[i].split()
        segs.append((int(t[0]), t[-2], t[-1]))
        i += 1
    nspin = 2 if spin == 1 else 1
    ks, evs = [], []
    while i < len(f) and f[i].strip():
        t = f[i].split()
        ks.append([float(t[1]), float(t[2]), float(t[3])])
        i += 1
        per = []
        for _ in range(nspin):
            v = []
            while len(v) < nb:
                v += [float(x) for x in f[i].split()]
                i += 1
            per.append(sorted(v))
        evs.append(per)
        if len(ks) >= sum(s[0] for s in segs):
            break
    # cartesian k distance
    d, dist = 0.0, [0.0]
    for j in range(1, len(ks)):
        p = [sum(ks[j][m] * b[m][c] for m in range(3)) for c in range(3)]
        q = [sum(ks[j - 1][m] * b[m][c] for m in range(3)) for c in range(3)]
        d += math.dist(p, q)
        dist.append(d)
    return nb, chemp, segs, dist, evs


nb, chemp, segs, dist, evs = read_band()
nk = len(dist)
DMAX = dist[-1]

ticks = [0]
acc = 0
for n, _, _ in segs:
    acc += n
    ticks.append(min(acc - 1, nk - 1))
labels = ["Γ"] + [s[2].replace("g", "Γ") for s in segs]


def bx(d):
    return BX0 + d / DMAX * (BX1 - BX0)


# ---------------------------------------------------------------- dos
SIGMA = 0.05        # eV, Gaussian smoothing of the raw tetrahedron DOS


def load(path):
    """Read a DOS/PDOS file, keep only the plotted window, sum both spins."""
    E, y = [], []
    for l in open(path):
        t = l.split()
        if len(t) >= 3:
            e = float(t[0])
            if EMIN - 6 * SIGMA <= e <= EMAX + 6 * SIGMA:
                E.append(e)
                y.append(float(t[1]) + abs(float(t[2])))
    return E, y


def smooth(E, y):
    """Gaussian convolution -- the tetrahedron DOS is single-point spiky."""
    if len(E) < 3:
        return y
    de = (E[-1] - E[0]) / (len(E) - 1)
    half = max(1, int(3 * SIGMA / de))
    ker = [math.exp(-0.5 * ((k * de) / SIGMA) ** 2) for k in range(-half, half + 1)]
    s = sum(ker)
    ker = [v / s for v in ker]
    n = len(y)
    out = []
    for i in range(n):
        a = 0.0
        for j, kv in enumerate(ker):
            m = i + j - half
            if 0 <= m < n:
                a += y[m] * kv
        out.append(a)
    return out


Ed, tot = load("test_1.DOS.Tetrahedron")
vac = [0.0] * len(Ed)
for a in VAC_MO:
    _, y = load("test_1.PDOS.Tetrahedron.atom%d" % a)
    vac = [vac[i] + y[i] for i in range(len(y))]
_, c13 = load("test_1.PDOS.Tetrahedron.atom%d" % CTRL_MO)

tot = smooth(Ed, tot)
vac = smooth(Ed, vac)
ctrl = [6 * v for v in smooth(Ed, c13)]

DMAXX = 1.06 * max(tot[i] for i in range(len(Ed)) if EMIN <= Ed[i] <= EMAX)


def dx(v):
    return DX0 + min(v, DMAXX) / DMAXX * (DX1 - DX0)


def dos_path(y, close):
    pts = [(dx(y[i]), ey(Ed[i])) for i in range(len(Ed)) if EMIN <= Ed[i] <= EMAX]
    if not pts:
        return ""
    p = "M %.1f %.1f " % (DX0, pts[0][1]) if close else "M %.1f %.1f " % pts[0]
    p += " ".join("L %.1f %.1f" % q for q in pts)
    if close:
        p += " L %.1f %.1f Z" % (DX0, pts[-1][1])
    return p


# ---------------------------------------------------------------- svg
o = []
o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
         'viewBox="0 0 %d %d" font-family="Helvetica,Arial,sans-serif">' % (W, H, W, H))
o.append('<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
o.append('<text x="%d" y="26" font-size="15" font-weight="600" fill="#111">'
         'MoS%s 4×4 monolayer, two S vacancies — bands and DOS (PBE)</text>'
         % (BX0, "₂"))

# defect level shading across both panels
yd0, yd1 = ey(0.66), ey(0.52)
for x0, x1 in ((BX0, BX1), (DX0, DX1)):
    o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="#f6d98a" '
             'fill-opacity="0.45"/>' % (x0, yd1, x1 - x0, yd0 - yd1))

# axes frames
for x0, x1 in ((BX0, BX1), (DX0, DX1)):
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
             'stroke="%s" stroke-width="1"/>' % (x0, Y0, x1 - x0, Y1 - Y0, C_AX))

# y grid + labels
e = EMIN
while e <= EMAX + 1e-9:
    y = ey(e)
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e6e9ee" '
             'stroke-width="1"/>' % (BX0, y, BX1, y))
    o.append('<text x="%d" y="%.1f" font-size="11" fill="#444" text-anchor="end">'
             '%+.0f</text>' % (BX0 - 8, y + 4, e))
    e += 1.0
o.append('<text x="24" y="%.1f" font-size="12" fill="#222" text-anchor="middle" '
         'transform="rotate(-90 24 %.1f)">E - E_F  (eV)</text>'
         % ((Y0 + Y1) / 2, (Y0 + Y1) / 2))

# band curves
for ib in range(nb):
    ys = [evs[k][0][ib] for k in range(nk)]
    if min(ys) * Ha - chemp * Ha > EMAX or max(ys) * Ha - chemp * Ha < EMIN:
        continue
    pts = []
    for k in range(nk):
        v = (ys[k] - chemp) * Ha
        if EMIN - 1 <= v <= EMAX + 1:
            pts.append("%.1f,%.2f" % (bx(dist[k]), ey(v)))
    if len(pts) < 2:
        continue
    dfct = (ib + 1) in DEFECT
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
             'stroke-opacity="%s"/>' % (" ".join(pts), C_DEF if dfct else C_HOST,
                                        "2.2" if dfct else "0.9",
                                        "1" if dfct else "0.75"))

# high symmetry ticks
for t, lab in zip(ticks, labels):
    x = bx(dist[t])
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
             'stroke-width="1"/>' % (x, Y0, x, Y1, C_AX))
    o.append('<text x="%.1f" y="%d" font-size="13" fill="#111" '
             'text-anchor="middle">%s</text>' % (x, Y1 + 20, lab))

# fermi level
for x0, x1 in ((BX0, BX1), (DX0, DX1)):
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#111" '
             'stroke-width="1.3" stroke-dasharray="6,4"/>' % (x0, ey(0), x1, ey(0)))
o.append('<text x="%d" y="%.1f" font-size="11" fill="#111">E_F</text>'
         % (BX1 - 30, ey(0) - 6))

# dos curves
o.append('<path d="%s" fill="%s" stroke="none"/>' % (dos_path(tot, True), C_TOT))
o.append('<path d="%s" fill="%s" fill-opacity="0.55" stroke="%s" '
         'stroke-width="1.1"/>' % (dos_path(vac, True), C_DEF, C_DEF))
o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.4" '
         'stroke-dasharray="5,3"/>' % (dos_path(ctrl, False), C_CTRL))
o.append('<text x="%.1f" y="%d" font-size="12" fill="#222" text-anchor="middle">'
         'DOS (states/eV)</text>' % ((DX0 + DX1) / 2, Y1 + 20))

# legend (opaque box so it never sits on top of a curve)
o.append('<rect x="%d" y="%d" width="176" height="60" fill="#ffffff" '
         'fill-opacity="0.92" stroke="#d5dae1" stroke-width="1" rx="3"/>'
         % (DX1 - 188, Y0 + 6))
lx, ly = DX1 - 176, Y0 + 24
for col, txt, dash in ((C_TOT, "total DOS", None),
                       (C_DEF, "Σ 6 Mo at vacancies", None),
                       (C_CTRL, "6 × Mo13 (unperturbed)", "5,3")):
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3" %s/>'
             % (lx, ly, lx + 22, ly, col,
                'stroke-dasharray="%s"' % dash if dash else ""))
    o.append('<text x="%d" y="%d" font-size="10.5" fill="#333">%s</text>'
             % (lx + 28, ly + 4, txt))
    ly += 16

# annotation
o.append('<text x="%.1f" y="%.1f" font-size="11" fill="#a03418" font-weight="600">'
         '4 S-vacancy levels</text>' % (BX0 + 12, ey(0.66) - 6))
o.append('<text x="%d" y="%d" font-size="10.5" fill="#555">'
         'VBM → defect levels = 0.996 eV  ·  VBM → host conduction band = 1.64 eV  ·  '
         'non-magnetic  ·  E_F = %.4f eV  ·  DOS Gaussian-broadened %.2f eV</text>'
         % (BX0, H - 22, chemp * Ha, SIGMA))
o.append("</svg>")

open("bands_dos.svg", "w").write("\n".join(o))
print("wrote bands_dos.svg  (%d bands, %d k-points, DMAX=%.4f)" % (nb, nk, DMAX))
