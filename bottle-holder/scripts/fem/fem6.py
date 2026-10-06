"""Module FEM with CalculiX's own frictionless contact against a rigid lift wall.

usage: fem6.py mesh.inp out_prefix      (env CASES=BUOY,HIT_TOP,...)
Same supports, loads and anisotropic criterion as fem4.py, but the one-sided wall contact is
solved by CalculiX (node-to-surface, linear penalty) against a fixed, very stiff plate lying on
the mounting plane, instead of an active-set loop (which flip-flops with quadratic tets).
Frictionless contact with zero initial gap is homogeneous in the load, so unit loads scale.
"""
import collections, json, os, subprocess, sys
import numpy as np
from fem_run import read_mesh, HOLES, AXIS, CCX
from fem2 import cases, E_IMPACT, BUOY
from fem3 import N, P0
from fem4 import fi_parts, X, Z, S, TEMP, SF, MODES

PEN = float(os.environ.get('PEN', '2e4'))      # MPa/mm contact stiffness


def wall_plate(nodes):
    """Hex plate on the mounting plane covering the face; returns new nodes, hexes."""
    e1 = np.array([0.0, 1.0, 0.0]); e2 = np.cross(N, e1); e2 /= np.linalg.norm(e2)
    pts = np.array(list(nodes.values()))
    on = pts[np.abs((pts - P0) @ N) < 0.5]
    a0, a1 = (on - P0) @ e1, (on - P0) @ e2
    A = np.arange(a0.min() - 4, a0.max() + 4.1, 3.0); B = np.arange(a1.min() - 4, a1.max() + 4.1, 3.0)
    nid0 = max(nodes) + 1; wn = {}; idx = {}
    for li, t in enumerate((0.0, 2.0)):
        for i, a in enumerate(A):
            for j, b in enumerate(B):
                wn[nid0] = P0 + a * e1 + b * e2 + t * N; idx[(li, i, j)] = nid0; nid0 += 1
    hexes = []
    for i in range(len(A) - 1):
        for j in range(len(B) - 1):
            c = [idx[(0, i, j)], idx[(0, i + 1, j)], idx[(0, i + 1, j + 1)], idx[(0, i, j + 1)],
                 idx[(1, i, j)], idx[(1, i + 1, j)], idx[(1, i + 1, j + 1)], idx[(1, i, j + 1)]]
            p = [wn[n] for n in c]
            if np.cross(p[1] - p[0], p[3] - p[0]) @ (p[4] - p[0]) < 0:
                c = [c[0], c[3], c[2], c[1], c[4], c[7], c[6], c[5]]
            hexes.append(c)
    return wn, hexes


def solve(path, nodes, tets, fixed, face, wn, hexes, loads):
    eid0 = max(tets) + 1
    with open(path + '.inp', 'w') as f:
        f.write('*HEADING\nrigid wall contact\n*NODE,NSET=ALLN\n')
        for n, p in nodes.items():
            f.write(f'{n},{p[0]:.9g},{p[1]:.9g},{p[2]:.9g}\n')
        f.write('*NODE,NSET=WALLN\n')
        for n, p in wn.items():
            f.write(f'{n},{p[0]:.9g},{p[1]:.9g},{p[2]:.9g}\n')
        f.write('*ELEMENT,TYPE=C3D10,ELSET=SOLID\n')
        for e, c in tets.items():
            f.write(f'{e},' + ','.join(map(str, c)) + '\n')
        f.write('*ELEMENT,TYPE=C3D8,ELSET=WALL\n')
        for k, c in enumerate(hexes):
            f.write(f'{eid0 + k},' + ','.join(map(str, c)) + '\n')
        for name, ids in (('FIX', fixed), ('FACE', sorted(face))):
            f.write(f'*NSET,NSET={name}\n' + '\n'.join(','.join(map(str, ids[i:i + 12])) for i in range(0, len(ids), 12)) + '\n')
        f.write('*SURFACE,NAME=SLAVE,TYPE=NODE\nFACE\n*SURFACE,NAME=MASTER\nWALL,S1\n')
        f.write('*MATERIAL,NAME=PETG\n*ELASTIC\n2200,0.38\n*MATERIAL,NAME=RIGID\n*ELASTIC\n2e6,0.3\n'
                '*SOLID SECTION,ELSET=SOLID,MATERIAL=PETG\n*SOLID SECTION,ELSET=WALL,MATERIAL=RIGID\n'
                f'*SURFACE INTERACTION,NAME=SI\n*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=LINEAR\n{PEN},0\n'
                '*CONTACT PAIR,INTERACTION=SI,TYPE=NODE TO SURFACE,ADJUST=0.002\nSLAVE,MASTER\n'
                '*BOUNDARY\nFIX,1,3\nWALLN,1,3\n*STEP,INC=200\n*STATIC\n0.25,1.0,1e-4,0.25\n*CLOAD\n')
        acc = collections.defaultdict(float)
        for w, comp, force in loads:
            for n, x in w.items():
                acc[(n, comp)] += force * x
        f.write(''.join(f'{n},{c},{v:.9g}\n' for (n, c), v in acc.items()))
        f.write('*NODE PRINT,NSET=ALLN,GLOBAL=YES\nU,RF\n*NODE PRINT,NSET=WALLN,GLOBAL=YES\nRF\n*EL PRINT,ELSET=SOLID\nS\n*END STEP\n')
    if not (os.environ.get('REUSE') and os.path.exists(path + '.dat')):
        r = subprocess.run([CCX, '-i', path], capture_output=True, env={'OMP_NUM_THREADS': '8'})
        out = r.stdout.decode(errors='ignore')
        if r.returncode or 'ERROR' in out:
            if 'too many cutbacks' not in out:
                raise RuntimeError(out[-1500:])
            print('  ccx stalled; using the last converged increment', flush=True)
    U, RF, FI, MODE, blk, t = {}, {}, collections.defaultdict(float), {}, None, 0.0
    for line in open(path + '.dat'):
        if 'time' in line and 'ALLN' in line.upper():
            t = float(line.split()[-1])
        if 'displacements' in line:
            blk = 'U'; U = {}; continue        # keep the last increment only
        if 'forces' in line:
            blk = 'F'; RF = {} if 'ALLN' in line.upper() else RF; continue
        if 'stresses' in line:
            blk = 'S'; FI = collections.defaultdict(float); MODE = {}; continue
        v = line.split()
        if not v or not v[0].isdigit():
            continue
        if blk == 'U':
            U[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif blk == 'F':
            RF[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif blk == 'S':
            e = int(v[0]); p = fi_parts(list(map(float, v[2:8]))); fv = float(np.sqrt((p ** 2).sum()))
            if fv > FI[e]:
                FI[e] = fv; MODE[e] = int(p.argmax())
    if t < 1.0 - 1e-9:                 # frictionless, zero-gap contact is homogeneous: scale up
        assert t > 0.3, t
        U = {n: v / t for n, v in U.items()}; RF = {n: v / t for n, v in RF.items()}
        FI = collections.defaultdict(float, {e: v / t for e, v in FI.items()})
        print(f'  scaled from load factor {t}', flush=True)
    return U, RF, FI, MODE


def main(mesh, out):
    nodes, tets, tris = read_mesh(mesh)
    fixed, per_hole = [], [0, 0]
    for n, p in nodes.items():
        for k, h in enumerate(np.array(HOLES)):
            t = (p - h) @ AXIS; r = np.linalg.norm((p - h) - t * AXIS)
            if 0.0 <= t <= 1.7 and abs(r - (4.6 - t)) < 0.3:
                fixed.append(n); per_hole[k] += 1; break
    fx = set(fixed)
    face = [n for n, p in nodes.items() if abs((p - P0) @ N) < 1e-3 and n not in fx]
    wn, hexes = wall_plate(nodes)
    print('seat nodes', per_hole, '| face nodes', len(face), '| wall hexes', len(hexes), flush=True)
    only = os.environ.get('CASES')
    cs = [c for c in cases(nodes, tris) if not only or c[0] in only.split(',')]
    eids = np.array(sorted(tets))
    cent = np.array([np.mean([nodes[n] for n in tets[e][:4]], axis=0) for e in eids])
    far = np.min(np.linalg.norm(cent[:, None] - np.array(HOLES)[None], axis=2), axis=1) > 7
    nid = np.array(sorted(nodes))
    res, fields, rend = {}, {}, {'disp': [], 'pc': [], 'comps': [], 'signs': [], 'screws': []}
    for name, kind, loads in cs:
        LM = 100.0 if kind == 'impact' else float(os.environ.get('LM_BUOY', 1.0))
        loads = [(w_, c_, f_ * LM) for w_, c_, f_ in loads]
        U, RF, FI, MODE = solve(out + '_' + name, nodes, tets, fixed, face, wn, hexes, loads)
        w, comp, force = loads[0]
        d = sum(U[n][comp - 1] * x for n, x in w.items()) * np.sign(force)
        if kind == 'impact':
            k = LM / d; F = (2 * E_IMPACT * k) ** 0.5; sc_ = F / LM
        else:
            k, F, sc_ = None, 1.0, 1.0 / LM
        util = np.array([FI[e] for e in eids]) * sc_ * SF[kind] / TEMP
        fields[name] = util
        j = int(np.argmax(np.where(far, util, 0)))
        bearing = sum(1 for n in face if RF.get(n) is not None and np.linalg.norm(RF[n]) > 1e-9)
        tot = sum((RF[n] for n in fixed), np.zeros(3)) + sum((RF[n] for n in face if n in RF), np.zeros(3))
        sc = []
        for h in np.array(HOLES):
            f = sum((RF[n] for n in fixed if np.linalg.norm(nodes[n] - h) < 8), np.zeros(3)) * sc_
            sc.append([round(float(f @ AXIS), 1), round(float(np.linalg.norm(f - (f @ AXIS) * AXIS)), 1)])
        res[name] = dict(k=k and round(k, 2), F=round(F if kind == 'impact' else 2 * BUOY, 1),
                         defl=round(d * sc_, 3), util=round(float(util[j]), 2),
                         mode=MODES[MODE[eids[j]]], at=[round(float(v), 1) for v in cent[j]],
                         screws_axial_lateral_N=sc)
        r = res[name]
        eq = sum((RF[n] for n in RF if n in nodes), np.zeros(3))
        eq = eq + sum((RF[n] for n in wn if n in RF), np.zeros(3))
        r['equilibrium_N'] = [round(float(v), 3) for v in eq]        # ccx RF on loaded nodes = the load; + seats + wall -> ~0
        print(f"{name:12s} sum RF {r['equilibrium_N']} (load {LM if kind == 'impact' else round(LM * 2 * BUOY, 1)} N) F {r['F']} N  k {r['k']}  defl {r['defl']} mm  FI/allow {r['util']} ({r['mode']}) at {r['at']}  "
              f"screws {sc}", flush=True)
        rend['disp'].append(np.array([U[n] * sc_ for n in nid]))
        rend['pc'].append(np.mean([nodes[n] for n in w], axis=0)); rend['comps'].append(comp); rend['signs'].append(np.sign(force))
        rend['screws'].append(sc)
    json.dump(res, open(out + '.json', 'w'), indent=1)
    nix = {n: i for i, n in enumerate(nid)}
    xyz = np.array([nodes[n] for n in nid])
    skin = np.array([[nix[n] for n in t[:3]] for t in tris if all(n in nix for n in t[:3])])
    np.savez(out + '.npz', cent=cent, far=far, names=list(fields), util=np.array(list(fields.values())),
             xyz=xyz, skin=skin, **{k: np.array(v) for k, v in rend.items()})


if __name__ == '__main__':
    main(*sys.argv[1:3])
