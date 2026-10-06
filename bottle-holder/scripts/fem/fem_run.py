"""Linear-elastic CalculiX run for one THD module. Units N, mm, MPa.

usage: fem_run.py mesh.inp out_prefix
Fixed: clamp disk r<=8 mm around both M4 axes through the rear wall.
Cases: BUOY +Z 5.886 N/bay, WEIGHT -Z 7 N/bay on the bay rim underside,
FRONT_DOWN -Z 50 N and FRONT_SIDE +Y 50 N on the front face (x = 61.5).
Writes <out>.npz: element centroids, von Mises per case, max |U| per case.
"""
import os
import subprocess
import sys
import collections
from pathlib import Path

import numpy as np

CCX = os.environ.get('CCX', '/Applications/FreeCAD.app/Contents/Resources/bin/ccx')   # CalculiX bundled with FreeCAD
HOLES = [np.array([-53.07, -19.75, -7.85]), np.array([-53.07, 63.75, -7.85])]
AXIS = np.array([-0.9914448613738105, 0.0, -0.13052619222005157])
BAYS = [(-36.75, 38.5), (41.5, 116.75)]


def read_mesh(path):
    nodes, tets, tris, kind = {}, {}, [], None
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith('**'):
            continue
        if line.startswith('*'):
            u = line.upper().replace(' ', '')
            kind = 'N' if u.startswith('*NODE') else 'T' if 'TYPE=C3D10' in u else \
                'S' if 'TYPE=CPS6' in u else None
            continue
        v = [x for x in line.replace(' ', '').split(',') if x]
        if kind == 'N':
            nodes[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif kind == 'T':
            tets[int(v[0])] = list(map(int, v[1:11]))
        elif kind == 'S':
            tris.append(list(map(int, v[1:7])))
    used = {n for t in tets.values() for n in t}
    return {n: p for n, p in nodes.items() if n in used}, tets, tris


def patch(nodes, tris, pick):
    """Consistent CPS6 loads: area/3 on each midside node; weights sum to 1."""
    w, area = collections.defaultdict(float), 0.0
    for t in tris:
        if not all(n in nodes for n in t):
            continue
        p = np.array([nodes[n] for n in t[:3]])
        if not pick(p):
            continue
        a = np.linalg.norm(np.cross(p[1] - p[0], p[2] - p[0])) / 2
        for n in t[3:6]:
            w[n] += a / 3
        area += a
    assert area > 5, area
    return {n: a / area for n, a in w.items()}, area


def main(mesh, out):
    nodes, tets, tris = read_mesh(mesh)
    fixed = []
    for n, p in nodes.items():
        for h in HOLES:
            r = p - h
            t = r @ AXIS
            if abs(t) <= 4 and np.linalg.norm(r - t * AXIS) <= 8:
                fixed.append(n)
                break
    rim = lambda p, lo, hi: (np.all(np.abs(p[:, 2] + 0.6) < 0.05)
                             and np.all((p[:, 1] > lo) & (p[:, 1] < hi)))
    front = lambda p: np.all(np.abs(p[:, 0] - 61.5) < 1e-3)
    bays = [patch(nodes, tris, lambda p, b=b: rim(p, *b)) for b in BAYS]
    fr, fr_area = patch(nodes, tris, front)
    cases = [('BUOY', [(w, 3, 5.886) for w, _ in bays]),
             ('WEIGHT', [(w, 3, -7.0) for w, _ in bays]),
             ('FRONT_DOWN', [(fr, 3, -50.0)]),
             ('FRONT_SIDE', [(fr, 2, 50.0)])]
    deck = Path(out + '.inp')
    with deck.open('w') as f:
        f.write('*HEADING\nTHD module; N mm MPa\n*NODE,NSET=ALLN\n')
        for n, p in nodes.items():
            f.write(f'{n},{p[0]:.9g},{p[1]:.9g},{p[2]:.9g}\n')
        f.write('*ELEMENT,TYPE=C3D10,ELSET=SOLID\n')
        for e, c in tets.items():
            f.write(f'{e},' + ','.join(map(str, c)) + '\n')
        f.write('*NSET,NSET=FIX\n')
        for i in range(0, len(fixed), 12):
            f.write(','.join(map(str, fixed[i:i + 12])) + '\n')
        f.write('*MATERIAL,NAME=PETG\n*ELASTIC\n2200,0.38\n'
                '*SOLID SECTION,ELSET=SOLID,MATERIAL=PETG\n*BOUNDARY\nFIX,1,3\n')
        for name, loads in cases:
            acc = collections.defaultdict(float)
            for w, comp, force in loads:
                for n, x in w.items():
                    acc[(n, comp)] += force * x
            f.write(f'** {name}\n*STEP\n*STATIC\n*CLOAD,OP=NEW\n')
            for (n, comp), v in acc.items():
                f.write(f'{n},{comp},{v:.9g}\n')
            f.write('*NODE PRINT,NSET=ALLN\nU\n*EL PRINT,ELSET=SOLID\nS\n*END STEP\n')
    subprocess.run([CCX, '-i', out], check=True, capture_output=True,
                   env={'OMP_NUM_THREADS': '8', 'PATH': '/usr/bin:/bin'})
    # parse .dat: per step a displacement block then a stress block
    eids = np.array(sorted(tets))
    index = {e: i for i, e in enumerate(eids)}
    vm, umax, block, step = [], [], None, -1
    for line in open(out + '.dat'):
        if 'displacements' in line:
            step += 1
            vm.append(np.zeros(len(eids)))
            umax.append(0.0)
            block = 'U'
            continue
        if 'stresses' in line:
            block = 'S'
            continue
        v = line.split()
        if not v or not v[0].isdigit():
            continue
        if block == 'U':
            umax[step] = max(umax[step], float(np.linalg.norm(list(map(float, v[1:4])))))
        elif block == 'S':
            sx, sy, sz, txy, txz, tyz = map(float, v[2:8])
            s = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2)
                        + 3 * (txy ** 2 + txz ** 2 + tyz ** 2))
            i = index[int(v[0])]
            vm[step][i] = max(vm[step][i], s)
    cent = np.array([np.mean([nodes[n] for n in tets[e][:4]], axis=0) for e in eids])
    np.savez(out + '.npz', cent=cent, vm=np.array(vm), umax=np.array(umax),
             names=[c[0] for c in cases])
    print(f'nodes {len(nodes)} tets {len(tets)} fixed {len(fixed)} rim {bays[0][1]:.0f}/{bays[1][1]:.0f} '
          f'front {fr_area:.0f} mm2')
    for (name, _), s, u in zip(cases, vm, umax):
        print(f'{name}: vm max {s.max():.2f} p99 {np.percentile(s, 99):.2f} MPa, |U| max {u:.3f} mm')


if __name__ == '__main__':
    main(*sys.argv[1:3])
