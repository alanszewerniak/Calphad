import glob, os
import MDAnalysis as mda
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation, PillowWriter

label = os.path.basename(glob.glob("*_zeolite.cif")[0]).split("_")[0]
u = mda.Universe("system.gro", "md.xtc")
n_fw = len(u.atoms) - 45
fw, co2 = u.atoms[:n_fw], u.atoms[n_fw:]
L = u.dimensions[:3]

fig = plt.figure(figsize=(7, 6.5))
ax = fig.add_subplot(111, projection="3d")
u.trajectory[0]
fwpos = fw.positions.copy()
ax.scatter(fwpos[::3, 0], fwpos[::3, 1], fwpos[::3, 2], s=4, c="0.6", alpha=0.25)
p0 = co2.positions
sc = ax.scatter(p0[:, 0], p0[:, 1], p0[:, 2], s=60, c="crimson", edgecolors="k", linewidths=0.4)
ax.set_xlim(0, L[0]); ax.set_ylim(0, L[1]); ax.set_zlim(0, L[2])
ax.set_xlabel("x (Angstrom)"); ax.set_ylabel("y (Angstrom)"); ax.set_zlabel("z (Angstrom)")
ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=18, azim=45)
ax.set_title("CO$_2$ diffusion in the %s-doped zeolite" % label, fontsize=13, weight="bold")
ax.text2D(0.5, 0.95, "Molecular dynamics,  298 K,  500 ps", transform=ax.transAxes,
          ha="center", fontsize=9, color="0.3")
leg = [Line2D([0],[0], marker='o', color='w', markerfacecolor='0.6', markersize=7, label='Framework'),
       Line2D([0],[0], marker='o', color='w', markerfacecolor='crimson', markersize=9, label='CO$_2$')]
ax.legend(handles=leg, loc="upper left", framealpha=0.9)

frames = range(0, len(u.trajectory), 10)
def update(i):
    u.trajectory[i]
    p = co2.positions
    sc._offsets3d = (p[:, 0], p[:, 1], p[:, 2])
    return sc,

ani = FuncAnimation(fig, update, frames=frames, blit=False)
out = "%s_diffusion.gif" % label
ani.save(out, writer=PillowWriter(fps=15), dpi=90)
print("wrote", out)
