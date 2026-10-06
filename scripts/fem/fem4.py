"""Module FEM: real bolt supports, one-sided wall contact, anisotropic FDM criterion.

usage: fem4.py mesh.inp out_prefix
Supports: each M4 screw = head seated on the 90 deg countersink (those surface nodes
fixed; the 6 mm bore has clearance and carries nothing), rear outer face in frictionless one-sided contact with
the lift wall (active set, see fem3.py).
Criterion (layers normal to model Z = print Z):
  FI = sqrt((vM_inplane / X)^2 + (max(szz,0) / Z)^2 + (tau_interlayer / S)^2)
with design strengths = TDS x 0.85 (38 C) / safety factor (2 impact, 4 sustained).
"""
import collections
import json
import os
import sys

import numpy as np

from fem_run import read_mesh, HOLES, AXIS
from fem2 import cases, E_IMPACT, BUOY
from fem3 import N, P0
import fem3

X, Z, S = 40.0, 20.0, 15.0        # PETG default (MPa): in-plane, interlayer tension, interlayer shear
TEMP = 0.85
SF = {'impact': 2.0, 'creep': 4.0}
MODES = ('in-plane', 'layer peel', 'layer shear')


def fi_parts(v):
    sx, sy, sz, txy, txz, tyz = v
    szc = min(sz, 0.0)
    vm = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - szc) ** 2 + (szc - sx) ** 2) + 3 * txy ** 2)
    return np.array([vm / X, max(sz, 0.0) / Z, np.hypot(txz, tyz) / S])


def solve(path, nodes, tets, fixed, held, loads):
    """fem3.solve but returning per-element max FI (characteristic) and its dominant mode."""
    U, RF, _ = fem3.solve(path, nodes, tets, fixed, held, loads)
    FI, MODE, blk = collections.defaultdict(float), {}, None
    for line in open(path + '.dat'):
        if 'stresses' in line:
            blk = 'S'; continue
        if 'displacements' in line or 'forces' in line:
            blk = None; continue
        v = line.split()
        if blk != 'S' or not v or not v[0].isdigit():
            continue
        e = int(v[0]); p = fi_parts(list(map(float, v[2:8])))
        f = float(np.sqrt((p ** 2).sum()))
        if f > FI[e]:
            FI[e] = f; MODE[e] = int(p.argmax())
    return U, RF, FI, MODE


def main(mesh, out):
    nodes, tets, tris = read_mesh(mesh)
    fixed, per_hole = [], [0, 0]
    for n, p in nodes.items():
        for k, h in enumerate(np.array(HOLES)):
            t = (p - h) @ AXIS
            r = np.linalg.norm((p - h) - t * AXIS)
            # head seat only: 90 deg countersink from the boss face (t = 0, r = 4.6) to r = 3.0;
            # the bore (6 mm for M4) has clearance, so it carries nothing
            if 0.0 <= t <= 1.7 and abs(r - (4.6 - t)) < 0.3:
                fixed.append(n); per_hole[k] += 1
                break
    fx = set(fixed)
    face = [n for n, p in nodes.items() if abs((p - P0) @ N) < 1e-3 and p[2] < -0.6 and n not in fx]
    print('fixed nodes per screw', per_hole, '| contact face nodes', len(face), flush=True)
    assert min(per_hole) > 20, per_hole
    only = os.environ.get('CASES')
    cs = [c for c in cases(nodes, tris) if not only or c[0] in only.split(',')]
    eids = np.array(sorted(tets))
    cent = np.array([np.mean([nodes[n] for n in tets[e][:4]], axis=0) for e in eids])
    far = np.min(np.linalg.norm(cent[:, None] - np.array(HOLES)[None], axis=2), axis=1) > 7
    res, fields = {}, {}
    for name, kind, loads in cs:
        held = set(face)
        for it in range(14):
            U, RF, FI, MODE = solve(out + '_' + name, nodes, tets, fixed, held, loads)
            pull = {n for n in held if RF[n] @ N > 1e-9}
            enter = {n for n in face if n not in held and U[n] @ N > 1e-6}
            if not pull and not enter:
                break
            held = (held - pull) | enter
        w, comp, force = loads[0]
        d = sum(U[n][comp - 1] * x for n, x in w.items()) * np.sign(force)
        if kind == 'impact':
            k = 1 / d; F = (2 * E_IMPACT * k) ** 0.5
        else:
            k, F = None, 1.0
        scale = F * SF[kind] / TEMP                     # characteristic FI -> utilisation
        util = np.array([FI[e] for e in eids]) * scale
        fields[name] = util
        j = int(np.argmax(np.where(far, util, 0)))
        res[name] = dict(k=k and round(k, 2), F=round(F if kind == 'impact' else 2 * BUOY, 1),
                         defl=round(d * F if kind == 'impact' else d, 3), util=round(float(util[j]), 2),
                         mode=MODES[MODE[eids[j]]], at=[round(float(v), 1) for v in cent[j]],
                         bearing=f'{len(held)}/{len(face)}', solves=it + 1)
        r = res[name]
        print(f"{name:12s} F {r['F']} N  k {r['k']}  defl {r['defl']} mm  FI/allow {r['util']} "
              f"({r['mode']}) at {r['at']}  contact {r['bearing']} ({r['solves']} solves)", flush=True)
    json.dump(res, open(out + '.json', 'w'), indent=1)
    np.savez(out + '.npz', cent=cent, far=far, names=list(fields), util=np.array(list(fields.values())))


if __name__ == '__main__':
    main(*sys.argv[1:3])
