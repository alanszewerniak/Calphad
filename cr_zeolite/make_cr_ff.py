import os, shutil
src = os.path.expanduser("~/Calphad/fe_zeolite/raspa/FeZeoliteFF")
dst = os.path.expanduser("~/Calphad/cr_zeolite/raspa/CrZeoliteFF")
os.makedirs(dst, exist_ok=True)
for f in os.listdir(src):
    shutil.copy(os.path.join(src, f), os.path.join(dst, f))
pa = os.path.join(dst, "pseudo_atoms.def")
lines = open(pa).read().splitlines()
lines = ["Cr    yes  Cr  Cr  0  51.9961   1.389    0.0  1.0  1.0   0  0  relative  0"
         if ln.split()[:1] == ["Fe"] else ln for ln in lines]
open(pa, "w").write("\n".join(lines) + "\n")
mr = os.path.join(dst, "force_field_mixing_rules.def")
lines = open(mr).read().splitlines()
lines = ["Cr              lennard-jones   7.54829   2.69319   // UFF"
         if ln.split()[:1] == ["Fe"] else ln for ln in lines]
open(mr, "w").write("\n".join(lines) + "\n")
print("built CrZeoliteFF at", dst)
