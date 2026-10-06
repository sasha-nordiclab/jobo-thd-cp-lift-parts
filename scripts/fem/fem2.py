"""THD module B: unit-load FEM -> buoyancy + energy-equivalent impact check.

usage: fem2.py mesh.inp out_prefix
Unit (1 N) cases; per case: compliance at the load patch -> stiffness k,
impact force F = sqrt(2 E k) (E = 0.35 J = 350 N mm), sigma = sigma_unit * F.
Clamp: disk r <= 8 mm around both M4 axes through the rear wall.
"""
import collections
import json
import subprocess
import sys

import numpy as np

from fem_run import read_mesh, patch, CCX, HOLES, AXIS

E_IMPACT = 87.5           # N mm (0.7 kg at 0.5 m/s)
BUOY = 1000 * 9.81 * 0.0006   # N per jar
ALLOW_IMPACT, ALLOW_CREEP = 8.5, 4.3
BAYS = [(-36.75, 38.5), (41.5, 116.75)]


def cases(nodes, tris):
    z, x, y = (lambda p: p[:, 2]), (lambda p: p[:, 0]), (lambda p: p[:, 1])
    ledge = lambda lo, hi: lambda p: (np.all(np.abs(z(p) + 0.8) < 0.02) and np.all((x(p) > 53.4) & (x(p) < 58.6))
                                      and np.all((y(p) > lo) & (y(p) < hi)))
    ztop = max(q[2] for q in nodes.values())
    top = lambda p: np.all(np.abs(z(p) - ztop) < 1e-3) and np.all((x(p) > 50) & (np.abs(y(p) - 0.9) < 10))
    front = lambda p: (np.all(np.abs(x(p) - 61.5) < 1e-3) and np.all(np.abs(y(p) - 0.9) < 10))
    div = lambda p: (np.all(np.abs(y(p) - 38.5) < 1e-3) and np.all((x(p) > 0) & (x(p) < 40))
                     and np.all((z(p) < -3) & (z(p) > -20)))
    return [('BUOY', 'creep', [(patch(nodes, tris, ledge(*b))[0], 3, BUOY) for b in BAYS]),
            ('HIT_TOP', 'impact', [(patch(nodes, tris, top)[0], 3, -1.0)]),
            ('HIT_FRONT', 'impact', [(patch(nodes, tris, front)[0], 1, -1.0)]),
            ('HIT_DIVIDER', 'impact', [(patch(nodes, tris, div)[0], 2, 1.0)])]


def main(mesh, out):
    nodes, tets, tris = read_mesh(mesh)
    fixed = [n for n, p in nodes.items()
             if any(abs((p - h) @ AXIS) <= 4 and np.linalg.norm((p - h) - ((p - h) @ AXIS) * AXIS) <= 8
                    for h in HOLES)]
    cs = cases(nodes, tris)
    with open(out + '.inp', 'w') as f:
        f.write('*HEADING\nunit cases\n*NODE,NSET=ALLN\n')
        for n, p in nodes.items():
            f.write(f'{n},{p[0]:.9g},{p[1]:.9g},{p[2]:.9g}\n')
        f.write('*ELEMENT,TYPE=C3D10,ELSET=SOLID\n')
        for e, c in tets.items():
            f.write(f'{e},' + ','.join(map(str, c)) + '\n')
        f.write('*NSET,NSET=FIX\n' + '\n'.join(','.join(map(str, fixed[i:i + 12]))
                                                for i in range(0, len(fixed), 12)) + '\n')
        f.write('*MATERIAL,NAME=PETG\n*ELASTIC\n2200,0.38\n'
                '*SOLID SECTION,ELSET=SOLID,MATERIAL=PETG\n*BOUNDARY\nFIX,1,3\n')
        for name, _, loads in cs:
            acc = collections.defaultdict(float)
            for w, comp, force in loads:
                for n, v in w.items():
                    acc[(n, comp)] += force * v
            f.write(f'** {name}\n*STEP\n*STATIC\n*CLOAD,OP=NEW\n' +
                    ''.join(f'{n},{c},{v:.9g}\n' for (n, c), v in acc.items()) +
                    '*NODE PRINT,NSET=ALLN\nU\n*EL PRINT,ELSET=SOLID\nS\n*END STEP\n')
    subprocess.run([CCX, '-i', out], check=True, capture_output=True, env={'OMP_NUM_THREADS': '8'})
    eids = np.array(sorted(tets))
    idx = {e: i for i, e in enumerate(eids)}
    vm, U, blk, st = [], [], None, -1
    for line in open(out + '.dat'):
        if 'displacements' in line:
            st += 1; vm.append(np.zeros(len(eids))); U.append({}); blk = 'U'; continue
        if 'stresses' in line:
            blk = 'S'; continue
        v = line.split()
        if not v or not v[0].isdigit():
            continue
        if blk == 'U':
            U[st][int(v[0])] = np.array(list(map(float, v[1:4])))
        else:
            sx, sy, sz, txy, txz, tyz = map(float, v[2:8])
            s = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (txy ** 2 + txz ** 2 + tyz ** 2))
            i = idx[int(v[0])]; vm[st][i] = max(vm[st][i], s)
    cent = np.array([np.mean([nodes[n] for n in tets[e][:4]], axis=0) for e in eids])
    far = np.min(np.linalg.norm(cent[:, None] - np.array(HOLES)[None], axis=2), axis=1) > 12
    res, scaled = {}, []
    for (name, kind, loads), s, u in zip(cs, vm, U):
        w, comp, force = loads[0]
        d = sum(u[n][comp - 1] * x for n, x in w.items()) * np.sign(force)   # mean patch displacement per N
        if kind == 'impact':
            k = 1 / d
            F = (2 * E_IMPACT * k) ** 0.5
            allow = ALLOW_IMPACT
        else:
            k, F, allow = None, 1.0, ALLOW_CREEP
        sig = s * F
        scaled.append(sig / allow)       # utilisation field
        res[name] = dict(k=k and round(k, 2), F=round(F if kind == 'impact' else 2 * BUOY, 1),
                         defl=round(d * F if kind == 'impact' else d, 3),
                         smax=round(float(sig[far].max()), 2), smax_clamp=round(float(sig.max()), 2),
                         util=round(float(sig[far].max() / allow), 2))
        print(f"{name:12s} k {res[name]['k']} N/mm  F {res[name]['F']} N  defl {res[name]['defl']} mm  "
              f"σmax {res[name]['smax']} (at clamp {res[name]['smax_clamp']}) MPa  util {res[name]['util']}")
    util = np.max(scaled, axis=0)
    # visualisation data: nodes, skin triangles, nodal von Mises / displacement per case
    nid = np.array(sorted(nodes)); nix = {n: i for i, n in enumerate(nid)}
    xyz = np.array([nodes[n] for n in nid])
    skin = np.array([[nix[n] for n in t[:3]] for t in tris if all(n in nix for n in t[:3])])
    acc = np.zeros((len(cs), len(nid))); cnt = np.zeros(len(nid))
    for e, conn in tets.items():
        for n in conn[:4]:
            cnt[nix[n]] += 1
    for k, (s, (name, kind, loads)) in enumerate(zip(vm, cs)):
        F = 1.0 if kind != 'impact' else res[name]['F']
        for e, conn in tets.items():
            for n in conn[:4]:
                acc[k, nix[n]] += s[idx[e]] * F
    nodal = acc / np.maximum(cnt, 1)
    disp = np.array([[U[k].get(n, np.zeros(3)) * (1.0 if cs[k][1] != 'impact' else res[cs[k][0]]['F'])
                      for n in nid] for k in range(len(cs))])
    pc = [np.mean([nodes[n] for n in loads[0][0]], axis=0) for _, _, loads in cs]
    np.savez(out + '.npz', cent=cent, util=util, far=far, per=np.array(scaled), xyz=xyz, skin=skin,
             nodal=nodal, disp=disp, fixed=np.array([nodes[n] for n in fixed]), pc=np.array(pc),
             names=[c[0] for c in cs], comps=[c[2][0][1] for c in cs], signs=[np.sign(c[2][0][2]) for c in cs])
    json.dump(res, open(out + '.json', 'w'), indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:3])
