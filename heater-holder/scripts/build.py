"""Rebuild THD_Heater_Holder from scratch in the running FreeCAD: the 220 V heater mock-up and the
PETG clamp for its rubber head. Every step is one fdmkit run() batch sent over XML-RPC; it stops at
the first ERR. The camera is kept across the rebuild.

  python3 scripts/build.py          closes the document and rebuilds everything
  python3 scripts/build.py 3        resumes from step 3 (document left open)

Coordinates: z = 0 is the bath floor (base glue face), the heater axis runs along X at z = ax_z,
x = 0 is the joint between the rubber head (x < 0) and the rod (x > 0).

Clamp: two bodies split at the axis with a gap k_gap.
Symmetry: each body is ONE sketch of its +Y half profile (DoF 0, every size from params), padded
symmetric about the head middle, its +Y screw hole and end chamfers, then ONE PartDesign Mirrored
(TransformMode "Whole shape") of the finished half across the XZ plane. The second screw is an App::Link.

- Base: a solid block on the floor with a half-round bed for the head and two blind octagonal M4 pilot holes;
  the screws form their own thread in the PETG. Printed on its glue face.
- Cap: a half ring with two flat ears and countersunk octagonal M4 clearance holes for
  ISO 14581 M4 x 16 screws from the Fasteners workbench. Printed on its end
  face x = -hd_l (profile on the bed), so the bore and the ears need no support.
Tightening the screws closes the gap and squeezes the rubber head; no snap, so heat swell is harmless.
"""
import os
import sys
import xmlrpc.client

URL = os.environ.get('FREECAD_RPC', 'http://127.0.0.1:9875')
MOD = os.path.expanduser('~/Library/Application Support/FreeCAD/v26-3/Mod/fdmkit')
HERE = os.path.dirname(os.path.abspath(__file__))
FCSTD = os.path.normpath(os.path.join(HERE, '..', 'cad', 'THD_Heater_Holder.FCStd'))
DOC = 'THD_Heater_Holder'

# (name, value or formula, description); None as name starts a group header
PARAMS = [
    (None, 'HEATER', None),
    ('rod_d', 16, 'Heating rod diameter'),
    ('rod_l', 110, 'Heating rod length from the head'),
    ('hd_d', 20, 'Rubber head diameter (the clamp grips here)'),
    ('hd_l', 20, 'Rubber head length'),
    ('ax_z', 15, 'Heater axis height above the bath floor'),
    (None, 'CLAMP', None),
    ('c_len', 'hd_l', 'Clamp length along the axis: the full head length'),
    ('c_fit', 0.2, 'Bore undersize on the soft rubber head (diametral)'),
    ('c_bw', 46, 'Width across the axis: base glue face and cap ears'),
    ('k_gap', 0.6, 'Gap between base and cap at the axis: the screws close it and squeeze the rubber'),
    ('k_t', 6, 'Cap ear thickness above the split: the countersink must clear the ring'),
    ('k_w', 3, 'Cap ring wall over the head (5 x 0.6)'),
    ('k_er', 1.5, 'Round on the outer top edges of the cap ears (stays clear of the countersink rim)'),
    (None, 'SCREWS M4 x 16 ISO 14581 (countersunk Torx, Fasteners WB)', None),
    ('s_len', 16, 'Screw length, head included (ISO 14581 measures overall)'),
    ('s_y', 16.5, 'Screw axis offset from the heater axis, across'),
    ('s_pd', 3.5, 'Octagonal pilot hole in the base, across flats: the M4 screw forms its thread in the flats'),
    ('s_pl', 12, 'Pilot hole depth from the base top'),
    ('s_cd', 4.5, 'Octagonal clearance hole in the cap ears, across flats'),
    ('s_kd', 9.6, 'Countersink diameter: ISO 14581 M4 dk theoretical 9.4 + 0.2 (Fasteners FsData/iso14581def.csv)'),
    ('s_ka', 90, 'Countersink angle, deg (ISO 14581 head)'),
    (None, 'BED CHAMFER', None),
    ('e_h', 1.2, 'Bed chamfer height along the print vertical (both parts stand on their end face x = -hd_l)'),
    ('e_a', 30, 'Bed chamfer angle from the print vertical, deg'),
    (None, 'DERIVED', None),
    ('c_bd', 'hd_d - c_fit', 'Bore diameter'),
    ('b_top', 'ax_z - k_gap / 2', 'Z of the base top (split face)'),
    ('k_bot', 'ax_z + k_gap / 2', 'Z of the cap bottom (split face)'),
    ('k_ro', 'c_bd / 2 + k_w', 'Cap ring outer radius'),
    ('k_top', 'k_bot + k_t', 'Z of the cap ear top (screw heads flush)'),
    ('e_w', 'e_h * tan(e_a * 1deg)', 'Bed chamfer width on the bed face'),
    ('b_pil', 'min(s_pl; b_top - 1.8)', 'Pilot depth actually cut: never closer than 1.8 mm to the glue face'),
    ('c_x', '-hd_l / 2', 'X of the clamp middle plane (head middle)'),
]


def params_batch():
    """All cells at once and one recompute. Values go in as formulas: the en_DK locale misreads
    plain decimals."""
    lines = ['import FreeCAD as App', 's = App.ActiveDocument.getObject("params")']
    for r, (name, val, desc) in enumerate(PARAMS, 1):
        if name is None:
            lines.append(f's.set("A{r}", {val!r}); s.setStyle("A{r}", "bold")')
        else:
            lines.append(f's.set("A{r}", {name!r}); s.set("B{r}", {"=" + str(val)!r}); s.setAlias("B{r}", {name!r}); s.set("C{r}", {desc!r})')
    lines += ['s.setColumnWidth("A", 110); s.setColumnWidth("C", 560)', 'App.ActiveDocument.recompute()',
              "P('c_bd', 'b_top', 'k_bot', 'k_ro')"]
    return '\n'.join(lines)


def new_body(name, color):
    return f'''import FreeCAD as App, FreeCADGui as Gui
d = App.ActiveDocument
b = d.addObject("PartDesign::Body", {name!r})
b.ViewObject.ShapeColor = {color!r}
Gui.getDocument(d.Name).ActiveView.setActiveObject("pdbody", b)
d.recompute()
"{name}: OK"'''


# octagonal hole, flat-to-flat f, centre (c_x, y): a flat faces +X (print up when the part stands on
# its end face x = -hd_l), so the top is a short bridge and the sides are 45 deg; the screw bites the
# flats and the corners take the chips. Sketch on an XY plane: sketch x = X, sketch y = Y.
def octagon(f, y):
    r = f'({f})/2/cos(22.5deg)'
    return [(f'c_x + {r}*cos({22.5 + 45*k}deg)', f'{y} + {r}*sin({22.5 + 45*k}deg)') for k in range(8)]


# Half profiles (+Y) in the YZ mid plane: sketch x = Y (>= 0, the mirror plane is x = 0), sketch y = Z.
# Written with the Sketcher API because they need arcs; every dimension is a params expression, DoF 0.
HALF_SKETCH_HEAD = '''import FreeCAD as App, Part, Sketcher, math
V, C = App.Vector, Sketcher.Constraint
d = App.ActiveDocument
P = d.getObject("params")
def p(n):
    v = P.get(n); return float(getattr(v, "Value", v))
def sketch(body, name, plane):
    b = d.getObject(body)
    s = b.newObject("Sketcher::SketchObject", name)
    s.AttachmentSupport = [(d.getObject(plane), "")]; s.MapMode = "FlatFace"
    return s
def line(s, a, b):
    return s.addGeometry(Part.LineSegment(V(*a, 0), V(*b, 0)))
def arc(s, c, r, a0, a1):
    return s.addGeometry(Part.ArcOfCircle(Part.Circle(V(*c, 0), V(0, 0, 1), r), a0, a1))
def dim(s, con, name, expr):
    i = s.addConstraint(con); s.renameConstraint(i, name); s.setExpression(f"Constraints.{name}", expr)
def done(s):
    d.recompute()
    dof = s.solve(); n = s.getGeometryFacade if False else None
    assert s.FullyConstrained, (s.Name, "not fully constrained", s.MalformedConstraints, s.Conflicting, s.Redundant)
    return f"{s.Name}: DoF 0, {s.ConstraintCount} constraints"
'''

# base half: bottom -> outer side -> top (split face) -> bed arc down to the axis line -> mirror line
BASE_HALF = '''
s = sketch("Base", "s_b_half", "b_mid")
r, w, zt, az = p("c_bd") / 2, p("c_bw") / 2, p("b_top"), p("ax_z")
yd = math.sqrt(r * r - (az - zt) ** 2)
l_bot = line(s, (0, 0), (w, 0))
l_side = line(s, (w, 0), (w, zt))
l_top = line(s, (w, zt), (yd, zt))
a_bed = arc(s, (0, az), r, -math.pi / 2, -math.asin((az - zt) / r))
l_mir = line(s, (0, az - r), (0, 0))
s.addConstraint([C("Coincident", l_bot, 1, -1, 1), C("Coincident", l_bot, 2, l_side, 1),
                 C("Coincident", l_side, 2, l_top, 1), C("Coincident", l_top, 2, a_bed, 2),
                 C("Coincident", a_bed, 1, l_mir, 1), C("Coincident", l_mir, 2, l_bot, 1),
                 C("Horizontal", l_bot), C("Vertical", l_side), C("Horizontal", l_top), C("Vertical", l_mir),
                 C("PointOnObject", a_bed, 3, -2)])
dim(s, C("DistanceX", l_bot, 1, l_bot, 2, w), "half_width", "params.c_bw / 2")
dim(s, C("DistanceY", l_side, 1, l_side, 2, zt), "base_top", "params.b_top")
dim(s, C("DistanceY", -1, 1, a_bed, 3, az), "axis_z", "params.ax_z")
dim(s, C("Radius", a_bed, r), "bed_r", "params.c_bd / 2")
done(s)'''

# cap half: bore arc from the split face up to the mirror line, split face, outer side, ear round,
# ear top, ring arc back to the mirror line
CAP_HALF = '''
s = sketch("Cap", "s_k_half", "k_mid")
r, ro, w, zb, ztop, az, er = (p(n) for n in ("c_bd", "k_ro", "c_bw", "k_bot", "k_top", "ax_z", "k_er"))
r, w = r / 2, w / 2
yg = math.sqrt(r * r - (zb - az) ** 2)
yk = math.sqrt(ro * ro - (ztop - az) ** 2)
a_bore = arc(s, (0, az), r, math.asin((zb - az) / r), math.pi / 2)
l_bot = line(s, (yg, zb), (w, zb))
l_side = line(s, (w, zb), (w, ztop - er))
a_round = arc(s, (w - er, ztop - er), er, 0, math.pi / 2)
l_top = line(s, (w - er, ztop), (yk, ztop))
a_ring = arc(s, (0, az), ro, math.asin((ztop - az) / ro), math.pi / 2)
l_mir = line(s, (0, az + ro), (0, az + r))
s.addConstraint([C("PointOnObject", a_bore, 3, -2), C("Coincident", a_ring, 3, a_bore, 3),
                 C("Coincident", a_bore, 1, l_bot, 1), C("Horizontal", l_bot),
                 C("Coincident", l_bot, 2, l_side, 1), C("Vertical", l_side),
                 C("Tangent", l_side, 2, a_round, 1), C("Tangent", a_round, 2, l_top, 1), C("Horizontal", l_top),
                 C("Coincident", l_top, 2, a_ring, 1), C("Coincident", a_ring, 2, l_mir, 1),
                 C("Coincident", l_mir, 2, a_bore, 2), C("Vertical", l_mir), C("PointOnObject", l_mir, 1, -2)])
dim(s, C("DistanceY", -1, 1, a_bore, 3, az), "axis_z", "params.ax_z")
dim(s, C("Radius", a_bore, r), "bore_r", "params.c_bd / 2")
dim(s, C("Radius", a_ring, ro), "ring_r", "params.k_ro")
dim(s, C("Radius", a_round, er), "ear_round", "params.k_er")
dim(s, C("DistanceY", -1, 1, l_bot, 1, zb), "split_z", "params.k_bot")
dim(s, C("DistanceX", -1, 1, l_bot, 2, w), "half_width", "params.c_bw / 2")
dim(s, C("DistanceY", -1, 1, l_top, 1, ztop), "ear_top", "params.k_top")
done(s)'''


def mirror_xz(body, name):
    """PartDesign Mirrored of the whole finished +Y half across the XZ plane (heater axis plane)."""
    return f'''import FreeCAD as App
d = App.ActiveDocument
b = d.getObject({body!r})
prev = b.Tip
mi = d.addObject("PartDesign::Mirrored", {name!r})
b.addObject(mi)
mi.TransformMode = "Whole shape"
if mi.BaseFeature != prev: mi.BaseFeature = prev
b.Tip = mi  # with no Originals the body does not move its Tip by itself
mi.MirrorPlane = ([f for f in b.Origin.OriginFeatures if f.Role == "XZ_Plane"][0], [""])
mi.Refine = True  # merge the coplanar faces where the two halves meet
d.recompute()
assert b.Tip == mi and mi.BaseFeature == prev, (b.Tip.Name, mi.BaseFeature)
prev.Visibility = False
f"{{mi.Name}}: valid {{mi.Shape.isValid()}} solids {{len(mi.Shape.Solids)}} V {{mi.Shape.Volume:.1f}}"'''


def bed_chamfer(body, name, x_expr='-hd_l'):
    """Chamfer on the half's edges in the end face x = x_expr (not the mirror-plane edge): e_h along X, e_w on the face."""
    return f'''import FreeCAD as App
d = App.ActiveDocument
b = d.getObject({body!r}); tip = b.Tip
x0 = d.getObject("params").evalExpression({x_expr!r})
x0 = float(getattr(x0, "Value", x0))
edges = [f"Edge{{i}}" for i, e in enumerate(tip.Shape.Edges, 1)
         if abs(e.BoundBox.XMin - x0) < 1e-6 and abs(e.BoundBox.XMax - x0) < 1e-6
         and not (abs(e.BoundBox.YMin) < 1e-6 and abs(e.BoundBox.YMax) < 1e-6)]  # not on the mirror plane
ch = b.newObject("PartDesign::Chamfer", {name!r})
ch.Base = (tip, edges)
ch.ChamferType = "Two distances"
ch.setExpression("Size", "params.e_h"); ch.setExpression("Size2", "params.e_w")
d.recompute()
def bed_y():
    f = [f for f in ch.Shape.Faces if abs(f.BoundBox.XMax - x0) < 1e-6 and abs(f.BoundBox.XMin - x0) < 1e-6][0]
    return round(f.BoundBox.YMax, 3)
y = bed_y()
if abs(y - 0.5 * float(d.getObject("params").get("c_bw")) + float(d.getObject("params").get("e_w"))) > 1e-3:
    ch.FlipDirection = True; d.recompute(); y = bed_y()
tip.Visibility = False
f"{{ch.Name}}: {{len(edges)}} edges, bed face y max {{y}}, valid {{ch.Shape.isValid()}}, tip {{b.Tip.Name}}"'''


STEPS = [
    # fresh document (fdmkit new: params sheet + body "Body")
    f'new({DOC!r}); import FreeCAD as App; App.ActiveDocument.saveAs({FCSTD!r})',
    params_batch(),
    # ================= heater mock-up (body "Body")
    "plane('pl_head','YZ','-hd_l'); sk('s_head','pl_head'); circ('s_head','hd_d',0,'ax_z'); pad('s_head','hd_l','head'); "
    "sk('s_rod','YZ'); circ('s_rod','rod_d',0,'ax_z'); pad('s_rod','rod_l','rod')",
    '''import FreeCAD as App
d = App.ActiveDocument
b = d.getObject("Body")
b.Label = "Heater"
b.ViewObject.ShapeColor = (0.78, 0.78, 0.80)
bb = b.Shape.BoundBox
f"heater x {bb.XMin:.2f}..{bb.XMax:.2f} z {bb.ZMin:.2f}..{bb.ZMax:.2f} V {b.Shape.Volume:.1f} valid {b.Shape.isValid()}"''',
    # ================= base: half profile (+Y) -> pad -> +Y pilot hole -> mirror of the whole half
    new_body('Base', (0.62, 0.84, 0.74)),
    "plane('b_mid','YZ','c_x')",
    HALF_SKETCH_HEAD + BASE_HALF,
    "pad('s_b_half','c_len','b_half',side='sym'); "
    f"plane('b_top_pl','XY','b_top'); sk('s_b_pilot','b_top_pl'); poly('s_b_pilot', {octagon('s_pd', 's_y')!r}); "
    "pocket('s_b_pilot','b_pil','b_pilot')",
    bed_chamfer('Base', 'b_bed_chamfer'),
    bed_chamfer('Base', 'b_top_chamfer', '0'),
    mirror_xz('Base', 'b_mirror'),
    # ================= cap: half profile (+Y) -> pad -> +Y screw hole -> mirror of the whole half
    new_body('Cap', (0.70, 0.78, 0.95)),
    "plane('k_mid','YZ','c_x')",
    HALF_SKETCH_HEAD + CAP_HALF,
    "pad('s_k_half','c_len','k_half',side='sym'); "
    "plane('k_hole_pl','XY','k_bot'); "
    f"sk('s_k_oct','k_hole_pl'); poly('s_k_oct', {octagon('s_cd', 's_y')!r}); pocket('s_k_oct','2*k_t','k_oct',side='sym'); "
    "plane('k_top_pl','XY','k_top'); sk('s_k_hole','k_top_pl'); circ('s_k_hole','s_cd','c_x','s_y'); "
    "import FreeCAD as App; d = App.ActiveDocument; b = d.getObject('Cap'); h = d.addObject('PartDesign::Hole', 'k_hole'); b.addObject(h); "
    "h.Profile = d.getObject('s_k_hole'); d.recompute(); h.Threaded = False; h.setExpression('Diameter', 'params.s_cd'); "
    "h.HoleCutType = 'Countersink'; h.setExpression('HoleCutDiameter', 'params.s_kd'); h.setExpression('HoleCutCountersinkAngle', 'params.s_ka'); "
    "h.DepthType = 'ThroughAll'; h.DrillPoint = 'Flat'; d.getObject('s_k_hole').Visibility = False; d.recompute(); "
    "(b.Tip.Name, h.Shape.isValid(), round(h.Shape.Volume, 1), h.getStatusString())",
    bed_chamfer('Cap', 'k_bed_chamfer'),
    bed_chamfer('Cap', 'k_top_chamfer', '0'),
    mirror_xz('Cap', 'k_mirror'),
    # screw on +Y from the Fasteners workbench, head flush with the ear top; the -Y one is a link
    '''import FreeCAD as App
import FastenersCmd
d = App.ActiveDocument
P = d.getObject("params")
a = d.addObject("Part::FeaturePython", "Screw")
FastenersCmd.FSScrewObject(a, "ISO14581", None)
FastenersCmd.FSViewProviderTree(a.ViewObject)
a.Diameter = "M4"
a.Length = str(int(P.s_len))
a.setExpression(".Placement.Base.x", "params.c_x")
a.setExpression(".Placement.Base.y", "params.s_y")
a.setExpression(".Placement.Base.z", "params.k_top")
l = d.addObject("App::Link", "Screw_Mirror")
l.LinkedObject = a
l.setExpression(".Placement.Base.x", "params.c_x")
l.setExpression(".Placement.Base.y", "-params.s_y")
l.setExpression(".Placement.Base.z", "params.k_top")
d.recompute()
l.Label = a.Label + "_Mirror"  # Fasteners relabels the screw on recompute
f"{a.Label}: z {a.Shape.BoundBox.ZMin:.2f}..{a.Shape.BoundBox.ZMax:.2f}; link at {tuple(round(v, 2) for v in l.Placement.Base)}"''',
    # finish: hide construction, show tips only, save, report
    '''import FreeCAD as App, Part
d = App.ActiveDocument
for o in d.Objects:
    if o.TypeId.startswith("PartDesign::") and o.TypeId != "PartDesign::Body" or o.TypeId == "Sketcher::SketchObject":
        o.Visibility = False
for n in ("Body", "Base", "Cap"):
    b = d.getObject(n); b.Visibility = True; b.Tip.Visibility = True
for n in ("Screw", "Screw_Mirror"):
    d.getObject(n).Visibility = True
d.recompute(); d.save()
h, ba, ca = (d.getObject(n).Shape for n in ("Body", "Base", "Cap"))
def probe(sh, z0, z1, y):
    ln = Part.makeLine(App.Vector(-10, y, z0), App.Vector(-10, y, z1))
    return round(sh.common(ln).Length, 2)
bad = [o.Name for o in d.Objects if "Invalid" in o.State or "Error" in o.State]
out = []
for n, s in (("base", ba), ("cap", ca)):
    bb = s.BoundBox
    out.append(f"{n} y {bb.YMin:.1f}..{bb.YMax:.1f} z {bb.ZMin:.2f}..{bb.ZMax:.2f} V {s.Volume:.0f} valid {s.isValid()} solids {len(s.Solids)}")
out.append(f"overlap heater/base {h.common(ba).Volume:.1f} heater/cap {h.common(ca).Volume:.1f} base/cap {ba.common(ca).Volume:.2f}")
out.append(f"material on screw axis: base {probe(ba, 0, 15, 16.5)} (expect 15-0.3-12=2.7) cap {probe(ca, 15, 30, 16.5)} (expect 0)")
out.append(f"bad {bad}")
" | ".join(out)''',
]


def rpc(code, timeout=300):
    r = xmlrpc.client.ServerProxy(URL, allow_none=True).execute_code(code, timeout)
    msg = r.get('message') or r.get('error') or str(r)
    return r.get('success'), msg.split('Output: ', 1)[-1].strip()


def run(expr):
    head = f'import sys\nsys.path.count({MOD!r}) or sys.path.insert(0, {MOD!r})\nimport fdmkit\n'
    ok, out = rpc(head + f'print(fdmkit.run({expr!r}))')
    return out if ok else 'RPC ERR ' + out


if __name__ == '__main__':
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if start == 0:
        ok, out = rpc(f'import FreeCAD as App, FreeCADGui as Gui\nif {DOC!r} in App.listDocuments():\n'
                      f'    App._fdm_cam = Gui.getDocument({DOC!r}).ActiveView.getCamera()\n    App.closeDocument({DOC!r})\n'
                      'print(list(App.listDocuments()))')
        print('close:', out)
    for i, expr in enumerate(STEPS[start:], start):
        out = run(expr)
        print(f'[{i}]', out[-600:])
        if 'ERR' in out:
            sys.exit(f'stopped at step {i}')
    # give the user back the camera they had before the rebuild (isometric fit on the first build)
    print('view:', rpc(f'''import FreeCAD as App, FreeCADGui as Gui
v = Gui.getDocument({DOC!r}).ActiveView
cam = getattr(App, "_fdm_cam", None)
if cam: v.setCamera(cam)
else: v.viewIsometric(); v.fitAll()
print("restored" if cam else "isometric")''')[1])
