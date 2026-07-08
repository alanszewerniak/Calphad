import os, shutil

src = os.path.expanduser("~/Calphad/fe_zeolite/raspa/FeZeoliteFF")
dst = os.path.expanduser("~/Calphad/ni_zeolite/raspa/NiZeoliteFF")
os.makedirs(dst, exist_ok=True)

# copy every file across first
for f in os.listdir(src):
    shutil.copy(os.path.join(src, f), os.path.join(dst, f))

# pseudo_atoms.def: turn the Fe row into a Ni row (mass 58.6934, charge 0.926)
pa = os.path.join(dst, "pseudo_atoms.def")
lines = open(pa).read().splitlines()
lines = ["Ni    yes  Ni  Ni  0  58.6934   0.926    0.0  1.0  1.0   0  0  relative  0"
         if ln.split()[:1] == ["Fe"] else ln for ln in lines]
open(pa, "w").write("\n".join(lines) + "\n")

# force_field_mixing_rules.def: swap the Fe Lennard-Jones line for Ni's UFF values
mr = os.path.join(dst, "force_field_mixing_rules.def")
lines = open(mr).read().splitlines()
lines = ["Ni              lennard-jones   7.54829   2.52481   // UFF"
         if ln.split()[:1] == ["Fe"] else ln for ln in lines]
open(mr, "w").write("\n".join(lines) + "\n")

print("built NiZeoliteFF at", dst)

#what is happening here is i'm opening the FeZeolite folder and copying all the files into a new folder
#reason being is because I am replacing the Fe2+ ions with the Ni2+ ions
#however i need to take into account the mass,size of the Ni2+ ions and how they differ from Fe2+ ions