import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation, PillowWriter
import glob, os

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
fwx = [p[0] for p in fw[::3]]; fwy = [p[1] for p in fw[::3]]; fwz = [p[2] for p in fw[::3]]
co2_path = glob.glob(os.path.join(D, "*component_CO2_0.pdb"))[0]
label = os.path.basename(co2_path).split("_")[1]
co2f = frames(co2_path)
up = UPTAKE.get(label)
Lmax = max(max(fwx), max(fwy), max(fwz))
leg = [Line2D([0],[0], marker='o', color='w', markerfacecolor='0.6', markersize=7, label='Framework'),
       Line2D([0],[0], marker='o', color='w', markerfacecolor='crimson', markersize=9, label='CO$_2$')]

fig = plt.figure(figsize=(7, 6.5))
ax = fig.add_subplot(111, projection="3d")
def update(i):
    ax.clear()
    ax.scatter(fwx, fwy, fwz, s=4, c="0.6", alpha=0.25)
    f = co2f[i]
    if f:
        ax.scatter([p[0] for p in f], [p[1] for p in f], [p[2] for p in f],
                   s=60, c="crimson", edgecolors="k", linewidths=0.4)
    ax.set_xlim(0, Lmax); ax.set_ylim(0, Lmax); ax.set_zlim(0, Lmax)
    ax.set_xlabel("x (Angstrom)"); ax.set_ylabel("y (Angstrom)"); ax.set_zlabel("z (Angstrom)")
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=18, azim=45)
    ax.set_title("CO$_2$ adsorption in the %s-doped zeolite" % label, fontsize=13, weight="bold")
    sub = "GCMC,  298 K,  1 bar" + ("     uptake = %.2f mol/kg" % up if up else "")
    ax.text2D(0.5, 0.95, sub, transform=ax.transAxes, ha="center", fontsize=9, color="0.3")
    ax.legend(handles=leg, loc="upper left", framealpha=0.9)
ani = FuncAnimation(fig, update, frames=len(co2f), blit=False)
out = "%s_co2_adsorption.gif" % label
ani.save(out, writer=PillowWriter(fps=3), dpi=90)
print("wrote", out)
