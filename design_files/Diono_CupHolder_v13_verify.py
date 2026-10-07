#!/usr/bin/env python3
"""Verification suite for Diono_CupHolder_v13 (run after Diono_CupHolder_v13.py).
Writes Diono_CupHolder_v13_verification.png and prints numeric checks."""
import os, re, zipfile
import numpy as np, trimesh, manifold3d as mf
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
H, AXIS = 88.9, np.array([50.42, 128.0])
def M(t): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))

def read3mf(path):
    x = zipfile.ZipFile(path).read('3D/3dmodel.model').decode()
    out = []
    for i, n, vs, ts in re.findall(r'<object id="(\d+)" name="([^"]+)".*?<vertices>(.*?)</vertices><triangles>(.*?)</triangles>', x, re.S):
        v = np.array(re.findall(r'x="([^"]+)" y="([^"]+)" z="([^"]+)"', vs), float)
        f = np.array(re.findall(r'v1="(\d+)" v2="(\d+)" v3="(\d+)"', ts), int)
        out.append((n, trimesh.Trimesh(v, f, process=False)))
    return out
def to_use(t):
    t = t.copy(); t.vertices[:, 0] -= AXIS[0]; t.vertices[:, 1] -= AXIS[1]; t.vertices[:, 2] = H - t.vertices[:, 2]; t.invert(); return t

v12 = read3mf(os.path.join(HERE, 'v12_base_for_generator.3mf'))
v13 = read3mf(os.path.join(HERE, 'Diono_CupHolder_v13_geometry.3mf'))
old, new = to_use(v12[0][1]), to_use(v13[0][1])
oldM, newM = M(old), M(new)
ok = True
def check(name, cond, info=''):
    global ok; ok &= bool(cond); print(('PASS ' if cond else 'FAIL ') + name + (('  ' + info) if info else ''))

# 1. file integrity (read back from the 3MF)
for n, t in v13:
    check(f'3MF object "{n}" watertight + consistent winding', t.is_watertight and t.is_winding_consistent and t.volume > 0, '%.1f mm3' % t.volume)
check('snap disc identical to v12', abs(v13[1][1].volume - v12[1][1].volume) < 0.01 and np.allclose(v13[1][1].bounds, v12[1][1].bounds))

# 5. boolean zone safety
BUMP_DROP = float(re.search(r'^BUMP_DROP = ([\d.]+)', open(os.path.join(HERE, 'Diono_CupHolder_v13.py'), encoding='utf-8').read(), re.M).group(1))
bump_zone = mf.Manifold.cylinder(3.0, 36.59, 36.59, 256).translate([0, 0, 4.0])
refM = (oldM - bump_zone) + (oldM ^ bump_zone).translate([0, 0, -BUMP_DROP])          # v12 with the snap bumps lowered
added, removed = newM - oldM, refM - newM          # removal judged against v12-with-lowered-bumps
post_zone = mf.Manifold.cube([10.0, 15.0, 19.0]).translate([39.0, -7.5, 27.0])
check('material removed only from the old gusset-post zone', (removed - post_zone).volume() < 0.5,
      'removed %.1f mm3, outside zone %.2f mm3' % (removed.volume(), (removed - post_zone).volume()))
hollow = mf.Manifold.cylinder(H - 1, 36.6, 36.6, 256).translate([0, 0, 0.5]) - refM
check('nothing added inside the bottle space (besides the lowered bumps)', ((newM - refM) ^ hollow).volume() < 0.5, '%.3f mm3' % ((newM - refM) ^ hollow).volume())
ring = mf.Manifold.cylinder(40, 40.6, 40.6, 256).translate([0, 0, 48]) - mf.Manifold.cylinder(42, 35.0, 35.0, 256).translate([0, 0, 47])
xr = ((newM ^ ring) - (oldM ^ ring)).volume() + ((oldM ^ ring) - (newM ^ ring)).volume()
check('upper (wide) bore unchanged', xr < 0.5, '%.3f mm3 differ' % xr)
low = mf.Manifold.cylinder(H + 2, 36.4, 36.4, 256).translate([0, 0, -1])
xl = ((newM ^ low) - (refM ^ low)).volume() + ((refM ^ low) - (newM ^ low)).volume()
check('lower bore + disc seat unchanged; bumps = v12 bumps lowered %.2f mm' % BUMP_DROP, xl < 0.5, '%.3f mm3 differ' % xl)

# disc fit (James 2026-10-06: v12 disc rattled): vertical play at each bump, measured in sections
from shapely.geometry import Polygon as SP, box as sbox
from shapely.ops import unary_union
from shapely.affinity import translate as stranslate
disc_use = v13[1][1].copy(); disc_use.apply_translation([-200, -60, 0])
def sec2(m, ang):
    t = np.radians(ang); nrm = np.array([-np.sin(t), np.cos(t), 0]); dr = np.array([np.cos(t), np.sin(t), 0])
    return unary_union([SP(np.c_[e @ dr, e[:, 2]]).buffer(0) for e in m.section(plane_origin=[0, 0, 0], plane_normal=nrm).discrete])
for ang in (60, 180, 300):
    c = sec2(new, ang); dsk = sec2(disc_use, ang).intersection(sbox(25, -1, 40, 6))
    seat, bump = c.intersection(sbox(30, -2, 40, 3.2)), c.intersection(sbox(30, 3.2, 40, 10))
    dzs = np.arange(-0.8, 0.8, 0.002)
    s = min(z for z in dzs if seat.intersection(stranslate(dsk, 0, z)).area < 1e-7)
    b = max(z for z in dzs if bump.intersection(stranslate(dsk, 0, z)).area < 1e-7)
    check('disc held without rattle at bump %d° (preload 0.05-0.20 mm)' % ang, 0.05 <= s - b <= 0.20, 'preload %.3f mm (negative = play)' % (s - b))
above = mf.Manifold.cube([300, 300, 10]).translate([-150, -150, H])
check('nothing above the rim', (added ^ above).volume() < 0.01)
# snap rod + Arm Elbow: beyond the pad face (x >= 66) at any height, plus x >= 55 above the brace arch (h >= 26), |y| < 12
rod = mf.Manifold.cube([40, 24, H + 2]).translate([66, -12, -1]) + mf.Manifold.cube([51, 24, H - 26 + 1]).translate([55, -12, 26])
check('snap rod / Arm Elbow unchanged', ((newM ^ rod) - (oldM ^ rod)).volume() + ((oldM ^ rod) - (newM ^ rod)).volume() < 0.5)

# floating-island scan (print orientation, 0.16 mm layers): the only island allowed is the v6 snap-rod ridge,
# which v12 also has and which printed fine unsupported (Bambu reports it as "floating regions")
from shapely.ops import unary_union as _uu
_zs = np.arange(0.08, H, 0.16); _prev = None; islands = []
for _z, _s in zip(_zs, v13[0][1].section_multiplane(plane_origin=[0, 0, 0], plane_normal=[0, 0, 1], heights=_zs)):
    if _s is None: _prev = None; continue
    _ps = list(_s.polygons_full)
    if _prev is not None:
        islands += [(p.centroid.x - AXIS[0], p.centroid.y - AXIS[1], H - _z) for p in _ps if p.area > 0.05 and not p.intersects(_prev)]
    _prev = _uu(_ps)
ridge_only = all(abs(x_ - 71.1) < 1.5 and abs(y_) < 2 and abs(h_ - 42.6) < 1.5 for x_, y_, h_ in islands)
check('no floating islands except the known v6 rod ridge', ridge_only and len(islands) <= 1, '%d island(s): %s' % (len(islands), [tuple(round(c, 1) for c in i) for i in islands]))
other_side = mf.Manifold.cube([100, 200, H + 2]).translate([-100, -100, -1])
check('cup unchanged on the side away from the arm (x < 0), apart from the lowered bump', ((newM ^ other_side) - (refM ^ other_side)).volume() + ((refM ^ other_side) - (newM ^ other_side)).volume() < 0.5)

# 3. exact dimensions from sections
s = new.section(plane_origin=[0, 0, 9.0], plane_normal=[0, 0, 1]); v = s.vertices[s.vertices[:, 0] > 40]
check('brace reaches 25 mm from the wall (x = 64)', abs(v[:, 0].max() - 64.0) < 0.05, 'x max %.2f' % v[:, 0].max())
s = new.section(plane_origin=[62.0, 0, 0], plane_normal=[1, 0, 0]); v = s.vertices[np.abs(s.vertices[:, 2] - 9) < 6]
sf = new.section(plane_origin=[63.95, 0, 0], plane_normal=[1, 0, 0]); vf = sf.vertices[np.abs(sf.vertices[:, 2] - 9) < 6]
check('pad 55 x 7 mm (width 2 mm in, height at the face)', abs(np.ptp(v[:, 1]) - 55) < 0.1 and abs(vf[:, 2].min() - 4) < 0.05 and abs(vf[:, 2].max() - 11) < 0.15,
      '%.2f wide, face h %.2f-%.2f' % (np.ptp(v[:, 1]), vf[:, 2].min(), vf[:, 2].max()))
s = new.section(plane_origin=[0, 0, 11.0], plane_normal=[0, 0, 1]); v = s.vertices[np.abs(s.vertices[:, 1]) < 6]
rodx = v[v[:, 0] > 66][:, 0].min() if (v[:, 0] > 66).any() else np.nan
check('snap rod clears the pad', rodx - 64 > 10, 'gap %.1f mm at h 11' % (rodx - 64))

# 4. area-continuity scan along the print axis (0.3 mm steps): look for waffles / hidden seams
cup_p = v13[0][1]
zs = np.arange(0.15, H, 0.3); areas = []
for z in zs:
    sec = cup_p.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    areas.append(sum(p.area for p in sec.to_2D()[0].polygons_full) if sec is not None else 0.0)
areas = np.array(areas); jumps = np.abs(np.diff(areas))
alt = np.sum((np.diff(areas)[:-1] * np.diff(areas)[1:] < 0) & (jumps[:-1] > 20) & (jumps[1:] > 20))
check('area scan: no alternating (waffled) layers', alt == 0, 'max step %.0f mm2 at z %.1f' % (jumps.max(), zs[np.argmax(jumps)]))

# self-supporting brace: no down-facing surface on the brace/arch flatter than 25.5 deg (print orientation; Bambu adds supports only < 25 deg)
fn_, tc_, A_ = cup_p.face_normals, cup_p.triangles_center, cup_p.area_faces
ux, uy, uh = tc_[:, 0] - AXIS[0], tc_[:, 1] - AXIS[1], H - tc_[:, 2]
bz = (ux > 39.2) & (uh < 72) & (np.abs(uy) < 40) & ~((np.abs(uy) < 11) & (uh > 30))
flat = (fn_[:, 2] < -np.cos(np.radians(25.5))) & (tc_[:, 2] > 0.3) & bz
check('brace + arch print without supports (no overhang flatter than 25.5 deg)', A_[flat].sum() < 1.0, '%.2f mm2' % A_[flat].sum())

# 7. lay-flat (print orientation, rim on the bed)
fn, fc = cup_p.face_normals, cup_p.triangles
down = (fn[:, 2] < -0.9) & (fc[:, :, 2].max(axis=1) < 0.15)
contact = cup_p.area_faces[down].sum(); cp = fc[down].reshape(-1, 3)
check('bed contact > 200 mm2', contact > 200, '%.0f mm2, footprint %.1f x %.1f mm' % (contact, np.ptp(cp[:, 0]), np.ptp(cp[:, 1])))
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')

# 2. section overlays: v12 (gray) vs v13 (orange)
fig, axs = plt.subplots(2, 4, figsize=(28, 14))
def ov(ax, origin, normal, cols, xl, yl, title):
    for mesh, c, lw, lab in [(old, '#888', 1.2, 'v12'), (new, '#d9480f', 1.8, 'v13')]:
        sec = mesh.section(plane_origin=origin, plane_normal=normal)
        if sec is None: continue
        for i, e in enumerate(sec.discrete): ax.plot(e[:, cols[0]], e[:, cols[1]], '-', c=c, lw=lw, label=lab if i == 0 else None)
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.legend(loc='upper right'); ax.set_title(title, fontsize=14)
ov(axs[0, 0], [0, 0, 0], [0, 1, 0], (0, 2), (-45, 90), (-2, 92), 'Section y = 0 (through arm, rod, bump at 180°)')
ov(axs[0, 1], [0, 15, 0], [0, 1, 0], (0, 2), (25, 75), (-2, 92), 'Section y = 15 (brace side, arm-to-cup arch)')
ov(axs[0, 2], [0, 0, 0], [0, 1, 0], (0, 2), (-42, -28), (-1, 12), 'Section y = 0, bump + disc seat (must match)')
ov(axs[0, 3], [0, 0, 9], [0, 0, 1], (0, 1), (-45, 70), (-45, 45), 'Plan h = 9 (brace)')
ov(axs[1, 0], [0, 0, 22], [0, 0, 1], (0, 1), (30, 70), (-38, 38), 'Plan h = 22 (arch #9)')
ov(axs[1, 1], [0, 0, 40], [0, 0, 1], (0, 1), (30, 75), (-25, 25), 'Plan h = 40 (arch #10, rod)')
ov(axs[1, 2], [0, 0, 70], [0, 0, 1], (0, 1), (30, 60), (-25, 25), 'Plan h = 70 (arm-to-cup arches #11)')
ax = axs[1, 3]; ax.plot(zs, areas, '-', c='#1c4e80'); ax.set_xlabel('print z (mm, rim on bed = 0)'); ax.set_ylabel('section area mm²')
ax.grid(alpha=.3); ax.set_title('Area-continuity scan (print orientation)', fontsize=14)
fig.suptitle('Diono Cup Holder v13: verification (gray = v12, orange = v13)   ' + ('ALL CHECKS PASSED' if ok else 'CHECKS FAILED'), fontsize=18, weight='bold')
plt.tight_layout(); fig.savefig(os.path.join(HERE, 'Diono_CupHolder_v13_verification.png'), dpi=70)
