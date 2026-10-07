#!/usr/bin/env python3
"""Diono car-seat cup holder v13 = v12 + brace that protects the Arm Elbow.

Builds from the delivered v12 3MF (cup + snap disc), kept as generator_input/v12_base_for_generator.3mf:
    python Diono_CupHolder_v13.py
Needs: pip install --user trimesh manifold3d shapely scipy scikit-image numpy matplotlib

Outputs (this folder):
    Diono_CupHolder_v13_geometry.3mf           plain geometry (cup + disc on the plate); the Bambu project is made by
                                               Diono_CupHolder_v13_bambu_project.py
    Diono_CupHolder_v13_Cup.stl                cup only, print orientation (rim on the bed)
    Diono_CupHolder_v13_SnapDisc.stl           snap disc (unchanged from v12)

Working coordinates ("use" coords): cup axis at the origin, arm along +x, h = height above the
cup bottom as installed. The cup prints upside down, so print z = 88.9 - h.

Dimension sources: all brace / arch dimensions are James's instructions (concept rev 7, 2026-10-05);
arch radii and fillet sizes marked "chosen" were picked by Claude and approved via the concept image.
"""
import os, re, zipfile, time
import numpy as np, trimesh, manifold3d as mf
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
from skimage.draw import polygon as dpoly
from skimage.measure import marching_cubes
from scipy.ndimage import distance_transform_edt as edt, label, gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "generator_input", "v12_base_for_generator.3mf")      # the delivered v12 cup + disc

# ---------------- v12 reference geometry (measured from the v12 file) ----------------
H = 88.9                      # cup height
AXIS = np.array([50.42, 128.0])   # cup axis in the v12 3MF plate layout
R_WALL, R_EMB = 39.0, 37.8    # lower outer wall radius; brace embed depth (bore is 36.6)

# ---------------- brace (James's instructions) ----------------
H0, H1 = 4.0, 11.0            # brace bottom / top: "4 mm from the bottom"; 7 mm thick (James 2026-10-06, was 10)
REACH = 25.0                  # pad face 25 mm out from the cup wall
HALF_W = 27.5                 # 55 mm wide
X_PAD = R_WALL + REACH
R_FLARE = 8.0                 # chosen: plan-view fillet where the brace sides meet the curved wall
R_LOW = 3.0                   # chosen: small fillet under the brace at the wall
# arch on top of the brace (#9), James 2026-10-06: "maintain an arch; increase the slope as much as you can without
# making it appear straight and to not require support". Concave profile from the pad's top edge to the wall:
#   h = H1 + Hm(y) * (A*t + (1-A)*t^N),  t = 0 at the pad face .. 1 at the wall,  Hm scaled by the local pad-to-wall span
# -> every arch surface >= ~45.6 deg from horizontal when printed rim-down (no supports needed), ~3 mm visible curve,
#    steepening to ~65 deg at the wall, then a 5 mm rolling-ball blend into the wall.
# 2026-10-06 rev: James rejected the 45-deg-min version as "a straight line" (only 2.9 mm of curve). Now a TRUE
# circular arch: slope ARCH_PHI1 at the pad edge, turning to vertical (tangent) at the wall -> 6.6 mm of curve, like the
# earlier R14 cove but taller. Min slope ~32 deg > Bambu's 25 deg support threshold -> still no supports.
ARCH_PHI1, ARCH_PHI2, ARCH_Q = 28.0, 90.0, 1.0   # 2026-10-06 "curve more": 28 deg start (Bambu supports < 25), corners keep it
ARCH_BLEND = 5.0

# ---------------- arm changes (James: replace gusset post / arm joins cup with smooth arches) ----------------
RP = 10.0                     # chosen: arch radius replacing the v6 gusset post (#10)
PW = 4.4                      # post half-width (kept from v6)
LP1, LP2 = np.array([48.0, 45.7]), np.array([58.0, 41.3])   # arm-block underside line (measured, x,h)
R_ARM = 8.0                   # chosen: arm-to-cup arch radius (#11)
PITCH = 0.25                  # voxel size for the arm arches

# ---------------- snap bumps (James 2026-10-06: disc snaps and holds but rattles) ----------------
# Measured on v12/v13: seated disc has ~0.35 mm vertical play at each bump (sinks 0.20 mm onto the 45° seat,
# lifts 0.15 mm before the 30° catch face). Lowering the 3 bumps (same 0.75 mm shape) by BUMP_DROP leaves
# ~0.10 mm preload: the catch faces press the disc onto its seat and centre it. Raise/lower in 0.05 mm steps:
# still rattles -> larger; too hard to press in -> smaller (0.35 = zero play).
BUMP_DROP = 0.50          # 2026-10-06: 0.45 still rattled a little on the real print -> +0.05 (preload ~0.15 mm)

# ---------------- steel screw bore (James 2026-10-07: "bore a hole within the centre of the snap rod and into the Arm Elbow") ----------------
# A straight M5 hole on the rod's own centre line, entering at the centre of the rod's nose end face and running up through
# the rod and the Arm Elbow into the sloped support wedge. A stainless M5 screw in it bridges the elbow so the arm can't snap.
# The rod centre line was measured from v12 (perpendicular sections; it is straight to 1e-7 mm): rod section 10.3 x 10.3 mm,
# >= 5.0 mm from the line to the outside all the way from s = 9 to s = 72 mm. The nose end face is only ~6 x 6 mm.
ROD_TIP = np.array([82.874, 0.0, 11.647])   # measured: centre of the rod's nose end face (use coords)
ROD_ANGLE = 57.40                            # measured: rod centre line, degrees up from horizontal, pointing in toward the cup
BORE_D = 4.5          # M5 x 0.8 thread-forming hole in PETG (thread 4.83-4.98 OD, ~4.02 core; prints ~0.1-0.2 mm under)
BORE_DEPTH = 62.0     # from the nose face: a 60 mm screw ends at h 62, 10 mm past the elbow; 2 mm spare; 50 mm screws fit too

# ---------------- helpers ----------------
def ccw(P):
    P = np.asarray(P, float); sa = 0.5*np.sum(P[:, 0]*np.roll(P[:, 1], -1)-np.roll(P[:, 0], -1)*P[:, 1])
    return P if sa > 0 else P[::-1]
def to_cs(poly):
    polys = [poly] if poly.geom_type == 'Polygon' else list(poly.geoms)
    loops = []
    for p in polys:
        loops.append(ccw(np.array(p.exterior.coords)[:-1]))
        for i in p.interiors: loops.append(ccw(np.array(i.coords)[:-1])[::-1])
    return mf.CrossSection(loops)
def M(t): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))
def T(Mm):
    m = Mm.to_mesh(); return trimesh.Trimesh(np.array(m.vert_properties)[:, :3], np.array(m.tri_verts), process=False)
def xz_prism(poly, y0, y1):
    """Extrude an (x, h) polygon across y0..y1."""
    return mf.Manifold.extrude(to_cs(poly), y1 - y0).rotate([90, 0, 0]).translate([0, y1, 0])
def fillet_poly(pts, radii, n=16):
    P = np.array(pts, float); N = len(P); out = []
    for i in range(N):
        p0, p1, p2 = P[i-1], P[i], P[(i+1) % N]; r = radii[i]
        if r <= 0: out.append(p1); continue
        u = (p0-p1)/np.linalg.norm(p0-p1); v = (p2-p1)/np.linalg.norm(p2-p1)
        ang = np.arccos(np.clip(u@v, -1, 1)); t = r/np.tan(ang/2)
        t = min(t, 0.49*np.linalg.norm(p0-p1), 0.49*np.linalg.norm(p2-p1)); rr = t*np.tan(ang/2)
        a = p1+u*t; b = p1+v*t; bis = (u+v)/np.linalg.norm(u+v); c = p1+bis*(rr/np.sin(ang/2))
        a0 = np.arctan2(*(a-c)[::-1]); a1 = np.arctan2(*(b-c)[::-1]); d = (a1-a0+np.pi) % (2*np.pi)-np.pi
        for k in range(n+1):
            th = a0+d*k/n; out.append(c+rr*np.array([np.cos(th), np.sin(th)]))
    return np.array(out)
def print_to_use(t):
    t = t.copy(); t.vertices[:, 0] -= AXIS[0]; t.vertices[:, 1] -= AXIS[1]; t.vertices[:, 2] = H - t.vertices[:, 2]; t.invert(); return t
def use_to_print(t):
    t = t.copy(); t.vertices[:, 2] = H - t.vertices[:, 2]; t.vertices[:, 0] += AXIS[0]; t.vertices[:, 1] += AXIS[1]; t.invert(); return t

# ---------------- 0. load v12 ----------------
x = zipfile.ZipFile(SRC).read('3D/3dmodel.model').decode()
objs = re.findall(r'<object id="(\d+)" name="([^"]+)".*?<vertices>(.*?)</vertices><triangles>(.*?)</triangles>', x, re.S)
def obj_mesh(vs, ts):
    v = np.array(re.findall(r'x="([^"]+)" y="([^"]+)" z="([^"]+)"', vs), float)
    f = np.array(re.findall(r'v1="(\d+)" v2="(\d+)" v3="(\d+)"', ts), int)
    return trimesh.Trimesh(v, f, process=False)
cup12_print = obj_mesh(*objs[0][2:]); disc12 = obj_mesh(*objs[1][2:])
assert 'Cup' in objs[0][1] and 'disc' in objs[1][1].lower()
cup12 = print_to_use(cup12_print)
cup12M = M(cup12); assert cup12M.status() == mf.Error.NoError
print('v12 cup volume %.1f mm3' % cup12M.volume())

# ---------------- 1. brace: plan outline blended into the curved wall ----------------
rect = box(20, -HALF_W, X_PAD, HALF_W)
F = unary_union([rect, Point(0, 0).buffer(R_WALL, quad_segs=256)]).buffer(R_FLARE, quad_segs=32).buffer(-R_FLARE, quad_segs=32)
F = F.intersection(rect.buffer(R_FLARE + 1, join_style=2)).intersection(box(-99, -99, X_PAD, 99))
F = F.buffer(-1.5, quad_segs=8).buffer(1.5, quad_segs=8)                       # round the pad-face corners
F = F.union(Point(0, 0).buffer(R_EMB, quad_segs=256).intersection(rect.buffer(R_FLARE + 1, join_style=2)))
brace = mf.Manifold.extrude(to_cs(F.difference(Point(0, 0).buffer(R_EMB, quad_segs=256))), H1 - H0).translate([0, 0, H0])

# small fillet under the brace (radial cove, limited to the brace outline)
FL = box(36.9, H0 - R_LOW, R_WALL + R_LOW, H0 + 0.5).difference(Point(R_WALL + R_LOW, H0 - R_LOW).buffer(R_LOW, quad_segs=48))
low_fillet = mf.Manifold.revolve(to_cs(FL), 720) ^ mf.Manifold.extrude(to_cs(F), R_LOW + 1).translate([0, 0, H0 - R_LOW - 0.5])

# full-width arch on top of the brace (#9): steep self-supporting concave arch, from the pad's top edge to the wall
def heightfield_solid(xs, ys, Hg, zbot):
    """Closed mesh: top surface z = Hg[i, j] over the (xs, ys) grid, flat bottom at zbot."""
    nx_, ny_ = len(xs), len(ys); Xg, Yg = np.meshgrid(xs, ys, indexing='ij')
    top = np.c_[Xg.ravel(), Yg.ravel(), Hg.ravel()]; bot = np.c_[Xg.ravel(), Yg.ravel(), np.full(nx_ * ny_, zbot)]
    V = np.vstack([top, bot]); off = nx_ * ny_; idx = lambda i, j: i * ny_ + j
    Fc = []
    for i in range(nx_ - 1):
        for j in range(ny_ - 1):
            a_, b_, c_, d_ = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
            Fc += [(a_, b_, c_), (a_, c_, d_), (a_ + off, c_ + off, b_ + off), (a_ + off, d_ + off, c_ + off)]
    def side(ring):
        out = []
        for k in range(len(ring) - 1):
            p0, p1 = ring[k], ring[k + 1]; out += [(p0, p0 + off, p1), (p1, p0 + off, p1 + off)]
        return out
    ring = [idx(i, 0) for i in range(nx_)] + [idx(nx_ - 1, j) for j in range(1, ny_)] + \
           [idx(i, ny_ - 1) for i in range(nx_ - 2, -1, -1)] + [idx(0, j) for j in range(ny_ - 2, -1, -1)]
    Fc += side(ring)
    t = trimesh.Trimesh(V, np.array(Fc), process=True)
    if t.volume < 0: t.invert()
    return t
xs_ = np.arange(24.0, X_PAD + 0.25 + 1e-9, 0.25); ys_ = np.arange(-38.0, 38.0 + 1e-9, 0.25)
Xa, Ya = np.meshgrid(xs_, ys_, indexing='ij')
a_w = np.hypot(Xa, Ya) - R_WALL; b_p = X_PAD - Xa                                 # distance to wall / to pad plane
tt = np.where(a_w + b_p > 1e-6, np.clip(b_p / np.maximum(a_w + b_p, 1e-6), 0, 1), 1.0)
_ph = np.radians(np.linspace(ARCH_PHI1, ARCH_PHI2, 4000))                          # circular-arc profile, normalised
_sx, _sh = np.sin(_ph[-1]) - np.sin(_ph[0]), np.cos(_ph[0]) - np.cos(_ph[-1])
arc_t, arc_h = (np.sin(_ph) - np.sin(_ph[0])) / _sx, (np.cos(_ph[0]) - np.cos(_ph)) / _sh
ARCH_HC = REACH * _sh / _sx                                                          # arch height at the centre (~48 mm)
Hm = ARCH_HC * ((np.hypot(X_PAD, Ya) - R_WALL) / REACH) ** ARCH_Q                  # partly keep the slope where the span is longer
Ha = np.minimum(H1 + Hm * np.interp(tt, arc_t, arc_h), 70.0)
arch9 = M(heightfield_solid(xs_, ys_, Ha, H1 - 0.5)) ^ mf.Manifold.extrude(to_cs(F), 64).translate([0, 0, H1 - 0.5])
arch9 = arch9 - mf.Manifold.cylinder(80, R_EMB, R_EMB, 256) - mf.Manifold.cylinder(40, 40.0, 40.0, 256).translate([0, 0, 45.5])

# ---------------- 2. gusset post -> smooth arch (#10) ----------------
def L(xx): return LP1[1] + (LP2[1] - LP1[1]) / (LP2[0] - LP1[0]) * (xx - LP1[0])
cut = Polygon([(R_WALL + 0.03, 27.0), (48.6, 27.0), (48.6, min(45.2, L(48.6) - 0.3))] +
              [(xx, min(45.2, L(xx) - 0.3)) for xx in np.linspace(48.6, R_WALL + 0.03, 20)])
post_cut = xz_prism(cut, -7.5, 7.5) - mf.Manifold.cylinder(60, R_WALL + 0.03, R_WALL + 0.03, 256)
cupM = cup12M - post_cut
# lower the 3 snap bumps by BUMP_DROP: lift out the slab holding them (bore r 36.6 + 0.4 mm of wall), drop it
bump_slab = cup12M ^ mf.Manifold.cylinder(3.0, 37.0, 37.0, 256).translate([0, 0, 4.0])      # h 4-7 holds the bumps (h 4.35-6.4)
cupM = cupM - mf.Manifold.cylinder(3.0, 36.59, 36.59, 256).translate([0, 0, 4.0])            # remove the old bumps only
cupM = cupM + bump_slab.translate([0, 0, -BUMP_DROP])
d = (LP2 - LP1) / np.linalg.norm(LP2 - LP1); nu = np.array([-d[1], d[0]])
if nu[1] < 0: nu = -nu
cx = R_WALL + RP; hc = LP1[1] + (-RP - (cx - LP1[0]) * nu[0]) / nu[1]
Tw = (R_WALL, hc); Ta = (cx + RP * nu[0], hc + RP * nu[1]); K = (R_WALL, L(R_WALL))
tri = Polygon([(36.9, hc - 0.01), (36.9, K[1] + 1.0), (Ta[0], Ta[1] + 1.0), Ta, Tw])
arch10 = xz_prism(tri.difference(Point(cx, hc).buffer(RP, quad_segs=96)), -PW, PW) - mf.Manifold.cylinder(60, 36.9, 36.9, 256)
arch10 = arch10 - mf.Manifold.cylinder(20, 40.0, 40.0, 256).translate([0, 0, 45.5])          # bore widens above h ~46
crevice = mf.Manifold.cube([47.5 - 37.0, 2 * PW, 50.0 - 44.5]).translate([37.0, -PW, 44.5])
crevice = crevice - mf.Manifold.cylinder(20, 39.95, 39.95, 256).translate([0, 0, 45.5]) - mf.Manifold.cylinder(60, 36.9, 36.9, 256)

# ---------------- 3. arm-to-cup arches (#11): rolling-ball closing of arm + cup body ----------------
EXT, DR = 12.7, 1.0
def zp(h): return H - h
Rw_o, Rn_o = 41.28 + DR, 38.0 + DR; Rw_i, Rn_i = 38.88 + DR, 35.6 + DR
zs0, zs1 = 26.18 + EXT, 30.2 + EXT; SH = 1.0
wall = [(Rw_i + 1.0, 0.0), (Rw_o - 0.6, 0.0), (Rw_o, 0.6), (Rw_o, zs0 + SH), (Rn_o, zs1 + SH), (Rn_o, H),
        (Rn_i - 3.0, H), (Rn_i, zp(3.0)), (Rn_i, zs1), (Rw_i, zs0), (Rw_i, 1.0)]
W = fillet_poly(wall, [0, 0, 0, 3.0, 4.0, 1.5, 0.4, 0, 2.0, 3.0, 0]); W[:, 1] = H - W[:, 1]      # v12 wall profile, use coords
body = mf.Manifold.revolve(mf.CrossSection([ccw(W)]), 360)
Wg = np.array(Polygon(W).buffer(0.12, quad_segs=8).exterior.coords)[:-1]                # grown: no skin left on the arm
arm = cupM - mf.Manifold.revolve(mf.CrossSection([ccw(Wg)]), 720)
arm = arm - mf.Manifold.cylinder(H + 2, 38.5, 38.5, 256).translate([0, 0, -1])            # drop the snap bumps
arm_parts = [q for q in arm.decompose() if q.volume() > 50]
arm = arm_parts[0]
for q in arm_parts[1:]: arm = arm + q

def voxelize(Mm, x0, y0, z0, nx, ny, nz, p):
    V = np.zeros((nx, ny, nz), bool)
    for k in range(nz):
        for P in Mm.slice(z0 + (k + 0.5) * p).to_polygons():
            P = np.asarray(P); rr, cc = dpoly((P[:, 0] - x0) / p - 0.5, (P[:, 1] - y0) / p - 0.5, shape=(nx, ny)); V[rr, cc, k] ^= True
    return V
t0 = time.time()
(x0, y0, z0), (x1, y1, z1) = (32, -28, 26), (64, 28, 91)
p = PITCH; nx, ny, nz = int((x1 - x0) / p), int((y1 - y0) / p), int((z1 - z0) / p); r = R_ARM
A = voxelize(arm, x0, y0, z0, nx, ny, nz, p); B = voxelize(body, x0, y0, z0, nx, ny, nz, p)
a = (edt(~A) * p).astype(np.float32); b = (edt(~B) * p).astype(np.float32)
S = A | B; pad = int(np.ceil(r / p)) + 2
Sp = np.pad(S, pad, constant_values=False)
dil = (edt(~Sp) * p) <= r
e = (edt(dil) * p)[pad:-pad, pad:-pad, pad:-pad].astype(np.float32)
del Sp, dil
near = (a < r + 0.5) & (b < r + 0.5)
Xg, Yg, Zg = np.meshgrid(x0 + (np.arange(nx) + 0.5) * p, y0 + (np.arange(ny) + 0.5) * p, z0 + (np.arange(nz) + 0.5) * p, indexing='ij')
near &= ~((Xg < 56) & (np.abs(Yg) < 5.0) & (Zg < 44.0))          # under the arm block: arch #10 already fills it
del Xg, Yg, Zg
free0 = (e > r) & ~S & near
labf, nf = label(free0); szf = np.bincount(labf.ravel()) * p ** 3
free = np.isin(labf, [i for i in range(1, nf + 1) if szf[i] >= 20.0])
d_free = (edt(~free) * p).astype(np.float32)
fld = gaussian_filter(np.where(near, np.maximum(r - e, d_free - 0.5), 10.0).astype(np.float32), 1.0)
vv, ff, _, _ = marching_cubes(np.pad(fld, 1, constant_values=10), 0.0, spacing=(p, p, p))
tm = trimesh.Trimesh(vv + np.array([x0, y0, z0]) - p / 2, ff[:, ::-1], process=True)
if tm.volume < 0: tm.invert()
inner_env = mf.Manifold.revolve(mf.CrossSection([ccw([(0, -1), (38.9, -1), (38.9, 46.5), (42.1, 50.5), (42.1, H + 1), (0, H + 1)])]), 360)
arch11 = (M(tm) - inner_env) ^ mf.Manifold.cube([200, 200, H - 0.6]).translate([-100, -100, 0])
print('arm arches built in %.0fs (%.0f mm3)' % (time.time() - t0, arch11.volume()))

# blend the brace arch (#9) into the wall: same rolling-ball closing, ball radius ARCH_BLEND, arch vs cup body only
t0 = time.time(); r = ARCH_BLEND
(x0, y0, z0), (x1, y1, z1) = (24, -40, 12), (66, 40, 64)
nx, ny, nz = int((x1 - x0) / p), int((y1 - y0) / p), int((z1 - z0) / p)
A = voxelize(arch9, x0, y0, z0, nx, ny, nz, p); B = voxelize(body, x0, y0, z0, nx, ny, nz, p)
a = (edt(~A) * p).astype(np.float32); b = (edt(~B) * p).astype(np.float32)
S = A | B; pad = int(np.ceil(r / p)) + 2
dil = (edt(~np.pad(S, pad, constant_values=False)) * p) <= r
e = (edt(dil) * p)[pad:-pad, pad:-pad, pad:-pad].astype(np.float32); del dil
near = (a < r + 0.5) & (b < r + 0.5)
free0 = (e > r) & ~S & near
labf, nf = label(free0); szf = np.bincount(labf.ravel()) * p ** 3
free = np.isin(labf, [i for i in range(1, nf + 1) if szf[i] >= 5.0])
d_free = (edt(~free) * p).astype(np.float32)
fld = gaussian_filter(np.where(near, np.maximum(r - e, d_free - 0.5), 10.0).astype(np.float32), 1.0)
vv, ff, _, _ = marching_cubes(np.pad(fld, 1, constant_values=10), 0.0, spacing=(p, p, p))
tm = trimesh.Trimesh(vv + np.array([x0, y0, z0]) - p / 2, ff[:, ::-1], process=True)
if tm.volume < 0: tm.invert()
arch9_blend = M(tm) - inner_env
print('brace-arch wall blend built in %.0fs (%.0f mm3)' % (time.time() - t0, arch9_blend.volume()))

# ---------------- 4. assemble ----------------
v13 = cupM + brace + low_fillet + arch9 + arch9_blend + arch10 + crevice + arch11
v13 = sorted(v13.decompose(), key=lambda q: -q.volume())[0]      # no simplify(): even 0.01 mm drift nudges the bore
v13_solid = v13                                                  # before the screw bore (for the checks below)

# screw bore: cylinder on the rod centre line, from 1 mm outside the nose face to BORE_DEPTH inside
ROD_DIR = np.array([-np.cos(np.radians(ROD_ANGLE)), 0.0, np.sin(np.radians(ROD_ANGLE))])
def rod_cyl(r, s0, s1, seg=96):
    """Cylinder of radius r on the rod centre line from s0 to s1 mm (s = 0 at the nose face, + toward the cup)."""
    c = mf.Manifold.cylinder(s1 - s0, r, r, seg).translate([0, 0, s0])             # along +z
    c = c.rotate([0, -(90 - ROD_ANGLE), 0])                                          # +z -> ROD_DIR
    return c.translate(list(ROD_TIP))
assert np.allclose(np.array(rod_cyl(1, 0, 10).bounding_box()).reshape(2, 3).mean(0), ROD_TIP + 5 * ROD_DIR, atol=0.05), 'bore direction'
screw_bore = rod_cyl(BORE_D / 2, -1.0, BORE_DEPTH)
v13 = v13 - screw_bore
v13_use = T(v13)

# ---------------- 5. assertions ----------------
assert v13_use.is_watertight and v13_use.is_winding_consistent and v13_use.volume > 0
assert sum(1 for q in v13.decompose() if q.volume() > 1) == 1, 'cup must be one solid'
lo, hi = v13_use.bounds
assert np.allclose([lo[2], hi[2]], [0.0, H], atol=0.05), (lo, hi)                    # height unchanged
assert abs(hi[0] - cup12.bounds[1][0]) < 0.05                                          # rod tip unchanged
bump_zone = mf.Manifold.cylinder(3.0, 36.59, 36.59, 256).translate([0, 0, 4.0])
ref = (cup12M - bump_zone) + (cup12M ^ bump_zone).translate([0, 0, -BUMP_DROP])        # v12 with the bumps lowered
hollow = mf.Manifold.cylinder(H - 1, 36.6, 36.6, 256).translate([0, 0, 0.5]) - ref
assert (v13 ^ hollow).volume() < 0.5, 'nothing may enter the bottle space'
bore = mf.Manifold.cylinder(H + 2, 36.4, 36.4, 256).translate([0, 0, -1])
assert ((v13 ^ bore) - (ref ^ bore)).volume() < 0.5 and ((ref ^ bore) - (v13 ^ bore)).volume() < 0.5, 'bore/seat changed (other than the lowered bumps)'
above_lip = mf.Manifold.cylinder(H - 3.2, 36.59, 36.59, 256).translate([0, 0, 3.2])  # above the 45° seat lip
bumps13 = v13 ^ above_lip
assert abs(bumps13.volume() - (cup12M ^ above_lip).volume()) < 0.5, 'bump volume must be unchanged'
assert abs(bumps13.bounding_box()[2] - (4.35 - BUMP_DROP)) < 0.06, 'bumps start at h %.2f' % bumps13.bounding_box()[2]
far = mf.Manifold.cube([40, 24, H + 2]).translate([66, -12, -1]) + mf.Manifold.cube([51, 24, H - 26 + 1]).translate([55, -12, 26])   # snap rod + elbow
assert ((v13_solid ^ far) - (cup12M ^ far)).volume() < 0.5 and ((cup12M ^ far) - (v13_solid ^ far)).volume() < 0.5, 'snap rod changed'
# screw bore: removes exactly the bore cylinder, all of it inside the arm (opens only at the nose face), >= 2.7 mm wall
bore_cut = v13_solid - v13
bore_in = rod_cyl(BORE_D / 2, 0.3, BORE_DEPTH)
assert (bore_in - v13_solid).volume() < 0.05, 'bore breaks out of the arm'
assert abs(bore_cut.volume() - (screw_bore ^ v13_solid).volume()) < 0.01 and (bore_cut - screw_bore).volume() < 0.01
assert (rod_cyl(BORE_D / 2 + 2.7, 9.0, BORE_DEPTH) - v13_solid).volume() < 0.05, 'bore wall thinner than 2.7 mm'
assert (v13 ^ rod_cyl(BORE_D / 2 - 0.01, 0.0, BORE_DEPTH - 0.01)).volume() < 0.01, 'bore not clear'
print('screw bore: %.1f mm dia x %.1f mm deep along the rod (%.1f deg), %.0f mm3 removed; nose face at h %.1f, bottom at h %.1f'
      % (BORE_D, BORE_DEPTH, ROD_ANGLE, bore_cut.volume(), ROD_TIP[2], (ROD_TIP + BORE_DEPTH * ROD_DIR)[2]))
pad_sec = v13_use.section(plane_origin=[X_PAD - 2.0, 0, 0], plane_normal=[1, 0, 0])   # 2 mm in: past the 1.5 mm corner rounds
pv = pad_sec.vertices; pv = pv[np.abs(pv[:, 2] - (H0 + H1) / 2) < 6]
print('pad section: width %.2f mm, h %.2f-%.2f' % (pv[:, 1].max() - pv[:, 1].min(), pv[:, 2].min(), pv[:, 2].max()))
assert abs((pv[:, 1].max() - pv[:, 1].min()) - 2 * HALF_W) < 0.1, 'pad width'
face_sec = v13_use.section(plane_origin=[X_PAD - 0.05, 0, 0], plane_normal=[1, 0, 0]).vertices      # at the pad face itself
fv = face_sec[np.abs(face_sec[:, 2] - (H0 + H1) / 2) < 6]
assert abs(fv[:, 2].min() - H0) < 0.05 and abs(fv[:, 2].max() - H1) < 0.15, 'pad face height %.2f-%.2f' % (fv[:, 2].min(), fv[:, 2].max())
assert abs(v13_use.bounds[1][0] - cup12.bounds[1][0]) < 0.05
print('v13 cup volume %.1f mm3 (+%.1f vs v12, ~%.0f g PETG at 100%%)' % (v13.volume(), v13.volume() - cup12M.volume(), v13.volume() / 1000 * 1.27))

# ---------------- 6. export (print orientation, P2S plate layout as v12) ----------------
cup_print = use_to_print(v13_use)
assert abs(cup_print.bounds[0][2]) < 0.01
cup_print.export(os.path.join(HERE, 'Diono_CupHolder_v13_Cup.stl'))
disc12.export(os.path.join(HERE, 'Diono_CupHolder_v13_SnapDisc.stl'))

def obj(i, name, t):
    vs = ''.join(f'<vertex x="{a:.4f}" y="{b_:.4f}" z="{c:.4f}"/>' for a, b_, c in t.vertices)
    ts = ''.join(f'<triangle v1="{a}" v2="{b_}" v3="{c}"/>' for a, b_, c in t.faces)
    return f'<object id="{i}" name="{name}" type="model"><mesh><vertices>{vs}</vertices><triangles>{ts}</triangles></mesh></object>'
def write3mf(path, title, objs_):
    res = ''.join(obj(i + 1, n, t) for i, (n, t) in enumerate(objs_)); items = ''.join(f'<item objectid="{i+1}"/>' for i in range(len(objs_)))
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<metadata name="Title">{title}</metadata><resources>{res}</resources><build>{items}</build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', ct); zf.writestr('_rels/.rels', rels); zf.writestr('3D/3dmodel.model', model)
write3mf(os.path.join(HERE, 'Diono_CupHolder_v13_geometry.3mf'), 'Diono cup holder v13',
         [('Cup v13 (prints upside down)', cup_print), ('Snap disc v12/v13', disc12)])
b_ = cup_print.bounds; db = disc12.bounds
assert b_[0][0] > 0 and b_[0][1] > 0 and b_[1][0] < 256 and b_[1][1] < 256, b_
assert not (db[0][0] < b_[1][0] and db[1][0] > b_[0][0] and db[0][1] < b_[1][1] and db[1][1] > b_[0][1]), 'parts overlap on the plate'
print('cup on plate x %.1f-%.1f, y %.1f-%.1f; disc x %.1f-%.1f, y %.1f-%.1f' % (b_[0][0], b_[1][0], b_[0][1], b_[1][1], db[0][0], db[1][0], db[0][1], db[1][1]))
print('done')
