#!/usr/bin/env python3
"""Images for v13 (run after Diono_CupHolder_v13.py): Diono_CupHolder_v13_views.png and print_orientation.png."""
import os
import numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
import re
BUMP_DROP = float(re.search(r'^BUMP_DROP = ([\d.]+)', open(os.path.join(HERE, 'Diono_CupHolder_v13.py'), encoding='utf-8').read(), re.M).group(1))
H, AX = 88.9, np.array([50.42, 128.0])

def rot(az, el):
    a, e = np.radians(az), np.radians(el)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ Rz

def render(meshes, az, el, W=900, Hh=900, scale=None, center=None, light=(-0.4, -1, 0.8)):
    """Small z-buffer rasterizer. meshes: [(trimesh, rgb or per-face rgb array)]. Camera looks along +y after rotation."""
    R = rot(az, el)
    allv = np.vstack([m.vertices for m, _ in meshes]) @ R.T
    if center is None: center = (allv.min(0) + allv.max(0)) / 2
    if scale is None: scale = 0.86 * min(W, Hh) / max(np.ptp(allv[:, 0]), np.ptp(allv[:, 2]))
    def proj(P):
        Q = np.atleast_2d(P) @ R.T - center
        return np.c_[W / 2 + Q[:, 0] * scale, Hh / 2 - Q[:, 2] * scale, Q[:, 1]]
    zb = np.full((Hh, W), np.inf); img = np.ones((Hh, W, 3))
    L = np.array(light, float); L /= np.linalg.norm(L)
    for m, col in meshes:
        P = proj(m.vertices); F = m.faces; n = m.face_normals @ R.T
        lam = 0.28 + 0.72 * np.clip(n @ L, 0, 1) + 0.12 * np.clip(-n[:, 1], 0, 1)
        cols = np.asarray(col, float); cols = np.broadcast_to(cols, (len(F), 3)) if cols.ndim == 1 else cols
        for fi in np.nonzero(n[:, 1] < 0.05)[0]:
            a, b, c = P[F[fi]]
            x0 = int(max(0, np.floor(min(a[0], b[0], c[0])))); x1 = int(min(W - 1, np.ceil(max(a[0], b[0], c[0]))))
            y0 = int(max(0, np.floor(min(a[1], b[1], c[1])))); y1 = int(min(Hh - 1, np.ceil(max(a[1], b[1], c[1]))))
            if x1 < x0 or y1 < y0: continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
            d = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
            if abs(d) < 1e-12: continue
            w1 = ((xs - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (ys - a[1])) / d
            w2 = ((b[0] - a[0]) * (ys - a[1]) - (xs - a[0]) * (b[1] - a[1])) / d
            w0 = 1 - w1 - w2; ins = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
            if not ins.any(): continue
            z = w0 * a[2] + w1 * b[2] + w2 * c[2]
            sub = zb[y0:y1 + 1, x0:x1 + 1]; upd = ins & (z < sub)
            sub[upd] = z[upd]; img[y0:y1 + 1, x0:x1 + 1][upd] = cols[fi] * lam[fi]
    zz = np.where(np.isinf(zb), 1e3, zb)
    edge = np.maximum(np.abs(np.diff(zz, axis=1, append=zz[:, -1:])), np.abs(np.diff(zz, axis=0, append=zz[-1:]))) > 1.5
    img[edge] *= 0.35
    return np.clip(img, 0, 1), proj

cup_p = trimesh.load(os.path.join(HERE, 'Diono_CupHolder_v13_Cup.stl'))
disc = trimesh.load(os.path.join(HERE, 'Diono_CupHolder_v13_SnapDisc.stl'))
use = cup_p.copy(); use.vertices[:, 0] -= AX[0]; use.vertices[:, 1] -= AX[1]; use.vertices[:, 2] = H - use.vertices[:, 2]; use.invert()
CUP = np.array((0.56, 0.63, 0.73)); DISC = np.array((0.93, 0.78, 0.45))
seated = disc.copy(); seated.apply_translation([-200, -60, 0])        # disc seated in the cup (use coords)

# ---------- multi-angle views, every element labelled (James 2026-10-06: always label the _views image) ----------
CUP_LB = np.array((0.66, 0.79, 0.88))                               # light blue PETG Matte (James's final colour)
def pol(a, r, h):
    t = np.radians(a); return (r * np.cos(t), r * np.sin(t), h)
LB = dict(fontsize=12, ha='left', va='center', bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#555', lw=0.8))
AR = dict(arrowstyle='-', color='#222', lw=1.0, shrinkA=0, shrinkB=0)
def snap(P):
    """Move approximate anchor points onto the nearest model surface."""
    q, _, _ = trimesh.proximity.closest_point(use, np.atleast_2d(np.array(P, float))); return q
def labels(ax, p, items):
    pts = snap([it[1] for it in items])
    for (txt, _, tx, ty), q3 in zip(items, pts):
        q = p(q3)[0]
        ax.plot(q[0], q[1], 'o', ms=5, mfc='#c2410c', mec='white', mew=1.0, zorder=6)
        ax.annotate(txt, xy=(q[0], q[1]), xytext=(tx, ty), arrowprops=AR, zorder=7, **LB)
cup_only = [(use, CUP_LB)]
panels = [
    ('Front 3/4 (seat side on the right)', cup_only, -35, 18, None, [
        ('Rim (0.6/1.0 mm chamfers)', pol(-125, 42.3, 88.6), 5, 70), ('Bottle opening', pol(150, 39.4, 88.4), 330, 30),
        ('Upper (wide) section', pol(-115, 42.3, 70), 5, 250), ('Shoulder', pol(-115, 40.6, 47), 5, 420),
        ('Lower (narrow) section', pol(-110, 39, 25), 5, 560), ('Bottom edge', pol(-80, 38.8, 0.5), 5, 860),
        ('Sloped support wedge', (54, -10, 62), 620, 90), ('Arm-to-cup arches (8 mm)', (41.6, -13.4, 72), 560, 160),
        ('Arm Elbow', (61, -6.6, 46), 660, 300), ('Snap rod', (74, -5.2, 26), 690, 560),
        ('Brace arch', (52, -14, 22), 330, 700), ('Brace side fillet (8 mm)', (37.5, -27.6, 7.5), 5, 760),
        ('Flat pad face 55 x 7 mm', (63.9, -8, 7.5), 540, 860)]),
    ('Rear 3/4', cup_only, 145, 18, None, [
        ('Smooth exterior (no slots)', pol(170, 39, 25), 560, 760), ('Snap rod tip', (82, 2, 13), 5, 840),
        ('Brace arch (far side)', (50, 16, 25), 5, 560), ('Rim', pol(150, 42.3, 88.6), 560, 90)]),
    ('Side elevation', cup_only, 0, 0, None, [
        ('Arm block', (45, -6.5, 47), 520, 120), ('Arch under arm block\n(replaced gusset post)', (41.5, -4.4, 38), 80, 420),
        ('Small ridge on rod (v6)', (71.6, -1.5, 42.3), 640, 300), ('Rod tip (chamfered)', (82, -3, 13), 650, 760),
        ('Brace arch (true arch, >= 28 deg)', (56, -20, 20), 60, 640), ('Brace 7 mm thick', (60, -27.5, 7.5), 300, 860),
        ('Arm-to-cup arch', (41.6, -13.4, 80), 80, 160)]),
    ('Top (disc removed)', cup_only, 0, 90, 'bumps', [
        ('Bottle opening (79.9 ID)', pol(120, 41.2, 88.9), 120, 120), ('Brace (55 mm wide)', (55, -20, 12), 560, 800),
        ('Mounting arm', (52, 0, 75), 600, 160)]),
    ('From below (disc seated)', [(use, CUP_LB), (seated, DISC)], -50, -25, None, [
        ('Snap disc (seated)', (0, 0, 2), 330, 800), ('Brace underside', (55, -10, 4), 600, 820),
        ('Fillet under brace (3 mm)', pol(-25, 39.7, 2.4), 5, 600), ('Bottom edge', pol(160, 38.9, 0.5), 5, 870)]),
    ('Brace close-up', cup_only, -20, 12, 'close', [
        ('Brace arch (curves from 28 deg to vertical)', (50, -14, 26), 5, 520), ('Flat pad face 55 x 7 mm', (63.9, -8, 7.5), 520, 860),
        ('Brace side fillet', (37.5, -27.6, 7.5), 5, 760), ('Arm-to-cup arch', (41.6, -13.4, 62), 5, 300),
        ('Arm Elbow', (61, -6.6, 46), 640, 200), ('Snap rod', (74, -5.2, 26), 700, 470)]),
]
fig, axs = plt.subplots(2, 3, figsize=(27, 18), facecolor='white')
for ax, (title, ms, az, el, mode, items) in zip(axs.ravel(), panels):
    if mode == 'close':
        img, p = render(ms, az, el, scale=10.0, center=np.array([52, 0, 26]) @ rot(az, el).T)
    else:
        img, p = render(ms, az, el)
    ax.imshow(img); ax.set_axis_off(); ax.set_title(title, fontsize=17, weight='bold')
    if mode == 'bumps':
        for ang in (60, 180, 300):
            q = p(np.array(pol(ang, 36.3, 6)))[0]
            ax.add_patch(plt.Circle((q[0], q[1]), 16, fill=False, ec='#c2410c', lw=2.5))
            t = p(np.array(pol(ang, 21, 6)))[0]
            ax.text(t[0], t[1], 'Snap bump\n%d deg' % ang, ha='center', va='center', fontsize=12, color='#c2410c', weight='bold')
    labels(ax, p, items)
    ax.set_xlim(0, 900); ax.set_ylim(900, 0)
fig.suptitle('Diono Cup Holder v13 (light blue PETG Matte): brace protects the Arm Elbow; arm joins the cup with smooth arches',
             fontsize=22, weight='bold')
fig.text(0.5, 0.015, '88.9 mm tall  |  brace 55 mm wide x 7 mm thick, 4-11 mm above the bottom, pad face 25 mm from the wall  |  '
         'snap bumps lowered %.2f mm (no rattle)  |  snap rod unchanged from v6/v12  |  disc (yellow) unchanged' % BUMP_DROP, ha='center', fontsize=14)
plt.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(os.path.join(HERE, 'Diono_CupHolder_v13_views.png'), dpi=72)

# ---------- print_orientation.png ----------
m = cup_p.copy(); m.apply_translation([-AX[0], -AX[1], 0])         # print pose: rim on the bed (z = 0)
fn, tri = m.face_normals, m.triangles
bed = (fn[:, 2] < -0.9) & (tri[:, :, 2].max(axis=1) < 0.15)
over = (fn[:, 2] < -0.7) & ~bed                                     # down-facing > 45° from vertical: needs support
under_brace = tri[:, :, 2].mean(axis=1) > 55
cols = np.tile(CUP, (len(m.faces), 1)); cols[over & under_brace] = (0.35, 0.55, 0.95); cols[bed] = (0.95, 0.55, 0.15)
fig, axs = plt.subplots(1, 3, figsize=(30, 11), facecolor='white')
for ax, (az, el, title) in zip(axs, [(-35, 22, '3D view (print pose)'), (0, 0, 'Front elevation (print pose)'),
                                     (-35, -40, 'Seen from below the plate: orange = bed contact, blue = would need support')]):
    grid = []
    for g in np.arange(-60, 101, 10):
        grid += [((g, -60, 0), (g, 60, 0)), ((-60, g if g <= 60 else 60, 0), (100, g if g <= 60 else 60, 0))]
    img, p = render([(m, cols)], az, el, scale=6.0 if el else 6.5, center=(np.array([20, 0, 44]) @ rot(az, el).T))
    ax.imshow(img)
    for a_, b_ in grid:
        pa, pb = p(np.array(a_))[0], p(np.array(b_))[0]
        ax.plot([pa[0], pb[0]], [pa[1], pb[1]], '-', c='#bbb', lw=0.6, zorder=0)
    ax.set_xlim(0, 900); ax.set_ylim(900, 0); ax.set_axis_off(); ax.set_title(title, fontsize=16, weight='bold')
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=(0.95, 0.55, 0.15), label='bed contact: rim face (%.0f mm2) + 5 mm brim' % m.area_faces[bed].sum()),
                    Patch(color=(0.35, 0.55, 0.95), label='overhang flatter than 45 deg (none on the brace)'),
                    Patch(color=CUP, label='prints unsupported (same as v12)')], loc='lower center', ncol=3, fontsize=14)
fig.suptitle('Print pose: cup UPSIDE DOWN, rim on the textured PEI plate (do not rotate).\n'
             'Easiest: open Diono_CupHolder_v13_Cup_and_SnapDisc.3mf in Bambu Studio (all settings are built in; no supports needed).\n'
             'Using the STL instead: press F, click the rim face; supports OFF; 5 mm outer brim.',
             fontsize=15, weight='bold')
plt.tight_layout(rect=(0, 0.06, 1, 0.9)); fig.savefig(os.path.join(HERE, 'print_orientation.png'), dpi=75)
print('images written')
