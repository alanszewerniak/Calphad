import os
p = os.path.expanduser("~/Calphad/ni_zeolite/Ni_zeolite.cif")
elems = {"Si", "Al", "O", "Ni"}
out = []
for ln in open(p):
    parts = ln.split()
    if len(parts) >= 7 and parts[0] in elems:
        parts[1] = parts[0]
        out.append("  " + "  ".join(parts))
    else:
        out.append(ln.rstrip("\n"))
open(p, "w").write("\n".join(out) + "\n")
print("relabelled Ni_zeolite.cif")
#It renames the cif atoms from pymatgen labels like T1 and Ni576 to plain Si, Al, O and Ni,
#so RASPA can match every atom to the force field instead of ignoring it.