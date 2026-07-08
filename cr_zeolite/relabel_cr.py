import os
p = os.path.expanduser("~/Calphad/cr_zeolite/Cr_zeolite.cif")
elems = {"Si", "Al", "O", "Cr"}
out = []
for ln in open(p):
    parts = ln.split()
    if len(parts) >= 7 and parts[0] in elems:
        parts[1] = parts[0]
        out.append("  " + "  ".join(parts))
    else:
        out.append(ln.rstrip("\n"))
open(p, "w").write("\n".join(out) + "\n")
print("relabelled Cr_zeolite.cif")
