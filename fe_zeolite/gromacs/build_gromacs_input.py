"""
Build GROMACS input (system.gro + topol.top + index.ndx) for CO2 in the Fe-zeolite.
Run inside the gromacs folder, next to Fe_zeolite.cif:  python3 build_gromacs_input.py
"""
import numpy as np
from ase import Atoms
from ase.io import read, write

# type: (mass, charge, sigma_nm, epsilon_kJmol)
P = {
    "SI": (28.0855,  0.2600, 0.23000, 0.182919),   # framework Si
    "AL": (26.9815,  0.7130, 0.23000, 0.182919),   # framework Al
    "OZ": (15.9994, -0.3590, 0.33000, 0.440669),   # framework O
    "FE": (55.8450,  0.9260, 0.25943, 0.054393),   # Fe cation (exact neutral charge)
    "CX": (12.0110,  0.6512, 0.27450, 0.248907),   # CO2 carbon
    "OX": (15.9994, -0.3256, 0.30170, 0.712408),   # CO2 oxygen
}
elem2type = {"Si": "SI", "Al": "AL", "O": "OZ", "Fe": "FE"}

N_CO2   = 15
CO2_CO  = 1.16
rng = np.random.default_rng(0)

# ---- framework ----
fw = read("Fe_zeolite.cif")
cell = fw.cell.lengths()
fpos = fw.get_positions()
ftype = [elem2type[s] for s in fw.get_chemical_symbols()]

# ---- place CO2: carbon AND both oxygens must clear the framework ----
def min_img_dist(p, q, box):
    d = p - q
    d -= box * np.round(d / box)
    return np.linalg.norm(d, axis=-1)

#p is the framework atom positions, all 624 of them, an array of x,y,z coordinates.
#q is one single position, the candidate spot where you are thinking of putting a CO2 carbon.
#box is the size of the unit cell in each direction, x, y, z.
#d is the difference, p minus q, so for every framework atom it is the vector pointing from your candidate spot to that atom. Its length is the distance.

#sentences

#The script reads the unit cell and all the framework atom positions (Si, Al, O, Fe), then drops CO2 molecules into the empty pore space,
#keeping each one clear of the framework and at least 4.5 Å from any CO2 already placed
#It is only setting sensible non-overlapping starting positions, the actual capture near the Fe happens later when the simulation lets the CO2 move.

carbons = []
oxys = []
tries = 0
while len(carbons) < N_CO2 and tries < 2000000:
    tries += 1
    c = rng.random(3) * cell
    if np.min(min_img_dist(fpos, c, cell)) < 3.5:
        continue
    if carbons and min(np.linalg.norm(c - np.array(carbons), axis=1)) < 4.5:
        continue
    for _ in range(60):
        ax = rng.normal(size=3); ax /= np.linalg.norm(ax)
        o1 = c + CO2_CO * ax
        o2 = c - CO2_CO * ax
        if np.min(min_img_dist(fpos, o1, cell)) < 3.3:
            continue
        if np.min(min_img_dist(fpos, o2, cell)) < 3.3:
            continue
        carbons.append(c)
        oxys.append((o1, o2))
        break
print("placed", len(carbons), "CO2 after", tries, "tries")

#loop that checks if the candidate position for a CO2 carbon is at least 3.0 A away from any framework atom, and at least 4.5 A away from any already placed CO2 atom.
#If it passes the check it adds the CO2 carbon position to the list of carbons

# ---- combined structure ----
combined = fw.copy()
for c, (o1, o2) in zip(carbons, oxys):
    combined += Atoms("COO", positions=[c, o1, o2])
write("system.gro", combined)
print("wrote system.gro")

# ---- topology ----
def atomtypes_block():
    s = "[ atomtypes ]\n; name  mass    charge  ptype  sigma(nm)   epsilon(kJ/mol)\n"
    for name, (m, q, sig, eps) in P.items():
        s += "%-4s  %8.4f  0.0000  A     %10.6f  %10.6f\n" % (name, m, sig, eps)
    return s + "\n"

top = "[ defaults ]\n; nbfunc  comb-rule  gen-pairs  fudgeLJ  fudgeQQ\n1  2  yes  0.5  0.5\n\n"
top += atomtypes_block()

top += "[ moleculetype ]\n; name  nrexcl\nFRM  1\n\n[ atoms ]\n"
top += "; id  type  resnr  resname  atom  cgnr  charge   mass\n"
for j, t in enumerate(ftype):
    m, q, sig, eps = P[t]
    top += "%d  %s  1  FRM  %s  %d  %8.4f  %8.4f\n" % (j + 1, t, t, j + 1, q, m)
top += "\n"

#builds a master table of each atom type with its mass, sigma and epsilon; sets the global rules ([ defaults ], comb-rule 2 to match RASPA)
#lists every framework atom as one frozen molecule called FRM
#each line carrying that atom's real charge and mass, with no bonds so the framework stays rigid


top += "[ moleculetype ]\n; name  nrexcl\nCO2  2\n\n[ atoms ]\n"
top += "1  CX  1  CO2  C  1  %8.4f  %8.4f\n" % (P["CX"][1], P["CX"][0])
top += "2  OX  1  CO2  O  2  %8.4f  %8.4f\n" % (P["OX"][1], P["OX"][0])
top += "3  OX  1  CO2  O  3  %8.4f  %8.4f\n" % (P["OX"][1], P["OX"][0])
top += "\n[ bonds ]\n; ai aj func  b0(nm)  kb\n1 2 1 0.116 400000.0\n1 3 1 0.116 400000.0\n"
top += "\n[ angles ]\n; ai aj ak func  th0  k\n2 1 3 1 180.0 1000.0\n"

top += "\n[ system ]\nFe zeolite with CO2\n\n[ molecules ]\nFRM  1\nCO2  %d\n" % len(carbons)

with open("topol.top", "w") as f:
    f.write(top)
print("wrote topol.top")

#the framwork used for the simulation is treated as a single rigid molecule (FRM), while each CO2 is treated as a flexible molecule with bonds and angles defined.

# ---- index file for freezing the framework ----
n_fw = len(fw)
n_tot = len(combined)
with open("index.ndx", "w") as f:
    f.write("[ System ]\n")
    f.write(" ".join(str(i + 1) for i in range(n_tot)) + "\n")
    f.write("[ Framework ]\n")
    f.write(" ".join(str(i + 1) for i in range(n_fw)) + "\n")
    f.write("[ MobileCO2 ]\n")
    f.write(" ".join(str(i + 1) for i in range(n_fw, n_tot)) + "\n")
print("wrote index.ndx")