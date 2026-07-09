import os, subprocess, glob, re
for m in ["Ni", "Cr"]:
    mix = os.path.expanduser("~/Calphad/%s_zeolite/raspa/mix" % m.lower())
    print("running", m, "...", flush=True)
    subprocess.run(["simulate"], cwd=mix)
    files = sorted(glob.glob(os.path.join(mix, "Output/System_0/output_*.data")))
    vals = re.findall(r"Average loading absolute \[mol/kg framework\]\s+([\-0-9.]+)", open(files[-1]).read()) if files else []
    print("  ", m, "-> CO2, CH4 (mol/kg):", vals, flush=True)
