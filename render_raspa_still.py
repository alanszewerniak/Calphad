import glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "Movies/System_0"
def frames(path):
    fr, cur = [], []
    for ln in open(path):
        if ln.startswith(("ATOM", "HETATM")):
            try:
                cur.append((float(ln[30:38]), float(ln[38:46]), float(ln[46:54])))
            except ValueError:
                pass
        elif ln.startswith("ENDMDL"):
            fr.append(cur); cur = []
    if cur:
        fr.append(cur)
    return fr

fw = frames(os.path.join(D, "Framework_0_final.pdb"))[0]
co2_path = glob.glob(os.path.join(D, "*component_CO2_0.pdb"))[0]
label = os.path.basename(co2_path).split("_")[1]
co2 = frames(co2_path)[-1]

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")
ax.scatter([p[0] for p in fw[::3]], [p[1] for p in fw[::3]], [p[2] for p in fw[::3]],
           s=2, c="lightgray", alpha=0.15)
if co2:
    ax.scatter([p[0] for p in co2], [p[1] for p in co2], [p[2] for p in co2], s=55, c="red")
ax.set_title("CO2 adsorbed in the %s-zeolite" % label)
out = "%s_raspa_still.png" % label
fig.savefig(out, dpi=120)
print("wrote", out)
