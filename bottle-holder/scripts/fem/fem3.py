"""Module FEM with the rear wall bearing on the rigid lift wall (unilateral contact).

usage: fem3.py mesh.inp out_prefix
Supports: M4 clamp disks (all DOF) + rear outer face (normal n) in frictionless
one-sided contact, solved per load case by an active-set loop:
  start with every face node held in n; release nodes the wall would pull
  (reaction tensile), re-add nodes that move into the wall; repeat to a fixed set.
Loads, energy-equivalent impact and allowables as in fem2.py.
Writes <out>.json (results) and <out>.npz (visualisation data, same keys as fem2).
"""
import collections
import json
import subprocess
import sys

import numpy as np

from fem_run import read_mesh, CCX, HOLES, AXIS
from fem2 import cases, E_IMPACT, BUOY, ALLOW_IMPACT, ALLOW_CREEP

N = np.array(AXIS)                     # outward normal of the rear mounting face
P0 = np.array([-58.47, 0.0, -0.6])     # a point on that face


def vonmises(v):
    sx, sy, sz, txy, txz, tyz = v
    return np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (txy ** 2 + txz ** 2 + tyz ** 2))


def solve(path, nodes, tets, fixed, held, loads):
    with open(path + '.inp', 'w') as f:
        f.write('*HEADING\ncontact iteration\n*NODE,NSET=ALLN\n')
        for n, p in nodes.items():
            f.write(f'{n},{p[0]:.9g},{p[1]:.9g},{p[2]:.9g}\n')
        f.write('*ELEMENT,TYPE=C3D10,ELSET=SOLID\n')
        for e, c in tets.items():
            f.write(f'{e},' + ','.join(map(str, c)) + '\n')
        for name, ids in (('FIX', fixed), ('PLATE', sorted(held))):
            f.write(f'*NSET,NSET={name}\n' + '\n'.join(','.join(map(str, ids[i:i + 12]))
                                                    for i in range(0, len(ids), 12)) + '\n')
        f.write(f'*TRANSFORM,NSET=PLATE,TYPE=R\n{N[0]},{N[1]},{N[2]},0,1,0\n')
        f.write('*MATERIAL,NAME=PETG\n*ELASTIC\n2200,0.38\n'
                '*SOLID SECTION,ELSET=SOLID,MATERIAL=PETG\n*BOUNDARY\nFIX,1,3\n')
        if held:
            f.write('PLATE,1,1\n')
        f.write('*STEP\n*STATIC\n*CLOAD\n')
        acc = collections.defaultdict(float)
        for w, comp, force in loads:
            for n, x in w.items():
                acc[(n, comp)] += force * x
        f.write(''.join(f'{n},{c},{v:.9g}\n' for (n, c), v in acc.items()))
        f.write('*NODE PRINT,NSET=ALLN,GLOBAL=YES\nU,RF\n*EL PRINT,ELSET=SOLID\nS\n*END STEP\n')
    subprocess.run([CCX, '-i', path], check=True, capture_output=True, env={'OMP_NUM_THREADS': '8'})
    U, RF, S, blk = {}, {}, collections.defaultdict(float), None
    for line in open(path + '.dat'):
        if 'displacements' in line:
            blk = 'U'; continue
        if 'forces' in line:
            blk = 'F'; continue
        if 'stresses' in line:
            blk = 'S'; continue
        v = line.split()
        if not v or not v[0].isdigit():
            continue
        if blk == 'U':
            U[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif blk == 'F':
            RF[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif blk == 'S':
            e = int(v[0]); S[e] = max(S[e], vonmises(list(map(float, v[2:8]))))
    return U, RF, S


def main(mesh, out):
    nodes, tets, tris = read_mesh(mesh)
    fixed = [n for n, p in nodes.items()
             if any(abs((p - h) @ AXIS) <= 4 and np.linalg.norm((p - h) - ((p - h) @ AXIS) * AXIS) <= 8
                    for h in np.array(HOLES))]
    fx = set(fixed)
    face = [n for n, p in nodes.items() if abs((p - P0) @ N) < 1e-3 and p[2] < -0.6 and n not in fx]
    cs = cases(nodes, tris)
    eids = np.array(sorted(tets)); idx = {e: i for i, e in enumerate(eids)}
    cent = np.array([np.mean([nodes[n] for n in tets[e][:4]], axis=0) for e in eids])
    far = np.min(np.linalg.norm(cent[:, None] - np.array(HOLES)[None], axis=2), axis=1) > 12
    res, per, nodal_all, disp_all = {}, [], [], []
    nid = np.array(sorted(nodes)); nix = {n: i for i, n in enumerate(nid)}
    for name, kind, loads in cs:
        held = set(face)
        for it in range(12):
            U, RF, S = solve(out + '_' + name, nodes, tets, fixed, held, loads)
            pull = {n for n in held if RF[n] @ N > 1e-9}          # wall would have to pull
            enter = {n for n in face if n not in held and U[n] @ N > 1e-6}   # moves into the wall
            if not pull and not enter:
                break
            held = (held - pull) | enter
        w, comp, force = loads[0]
        d = sum(U[n][comp - 1] * x for n, x in w.items()) * np.sign(force)
        if kind == 'impact':
            k = 1 / d; F = (2 * E_IMPACT * k) ** 0.5; allow = ALLOW_IMPACT
        else:
            k, F, allow = None, 1.0, ALLOW_CREEP
        sig = np.array([S[e] for e in eids]) * F
        per.append(sig / allow)
        res[name] = dict(k=k and round(k, 2), F=round(F if kind == 'impact' else 2 * BUOY, 1),
                         defl=round(d * F if kind == 'impact' else d, 3),
                         smax=round(float(sig[far].max()), 2), smax_clamp=round(float(sig.max()), 2),
                         util=round(float(sig[far].max() / allow), 2),
                         contact=f'{len(held)}/{len(face)} nodes bearing after {it + 1} solves')
        acc = np.zeros(len(nid)); cnt = np.zeros(len(nid))
        for e, conn in tets.items():
            for n in conn[:4]:
                acc[nix[n]] += sig[idx[e]]; cnt[nix[n]] += 1
        nodal_all.append(acc / np.maximum(cnt, 1))
        disp_all.append(np.array([U[n] * F for n in nid]))
        r = res[name]
        print(f"{name:12s} k {r['k']} F {r['F']} N defl {r['defl']} mm σmax {r['smax']} "
              f"(clamp {r['smax_clamp']}) util {r['util']} | {r['contact']}", flush=True)
    xyz = np.array([nodes[n] for n in nid])
    skin = np.array([[nix[n] for n in t[:3]] for t in tris if all(n in nix for n in t[:3])])
    pc = [np.mean([nodes[n] for n in loads[0][0]], axis=0) for _, _, loads in cs]
    np.savez(out + '.npz', cent=cent, util=np.max(per, axis=0), far=far, per=np.array(per), xyz=xyz,
             skin=skin, nodal=np.array(nodal_all), disp=np.array(disp_all),
             fixed=np.array([nodes[n] for n in fixed]), pc=np.array(pc), names=[c[0] for c in cs],
             comps=[c[2][0][1] for c in cs], signs=[np.sign(c[2][0][2]) for c in cs])
    json.dump(res, open(out + '.json', 'w'), indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:3])
