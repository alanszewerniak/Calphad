import glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

UPTAKE = {"Fe": 5.11, "Ni": 5.07, "Cr": 6.16}
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

fig = plt.figure(figsize=(7, 6.5))
ax = fig.add_subplot(111, projection="3d")
ax.scatter([p[0] for p in fw[::3]], [p[1] for p in fw[::3]], [p[2] for p in fw[::3]],
           s=4, c="0.6", alpha=0.25)
if co2:
    ax.scatter([p[0] for p in co2], [p[1] for p in co2], [p[2] for p in co2],
               s=60, c="crimson", edgecolors="k", linewidths=0.4)
ax.set_xlabel("x (Angstrom)"); ax.set_ylabel("y (Angstrom)"); ax.set_zlabel("z (Angstrom)")
ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=18, azim=45)
ax.set_title("CO$_2$ adsorbed in the %s-doped zeolite" % label, fontsize=13, weight="bold")
up = UPTAKE.get(label)
sub = "GCMC,  298 K,  1 bar" + ("     uptake = %.2f mol/kg" % up if up else "")
ax.text2D(0.5, 0.95, sub, transform=ax.transAxes, ha="center", fontsize=9, color="0.3")
leg = [Line2D([0],[0], marker='o', color='w', markerfacecolor='0.6', markersize=7, label='Framework'),
       Line2D([0],[0], marker='o', color='w', markerfacecolor='crimson', markersize=9, label='CO$_2$')]
ax.legend(handles=leg, loc="upper left", framealpha=0.9)
out = "%s_raspa_still.png" % label
fig.savefig(out, dpi=150, bbox_inches="tight")
print("wrote", out)
