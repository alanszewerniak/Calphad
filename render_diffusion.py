import glob, os
import MDAnalysis as mda
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

label = os.path.basename(glob.glob("*_zeolite.cif")[0]).split("_")[0]
u = mda.Universe("system.gro", "md.xtc")
n_fw = len(u.atoms) - 45
fw, co2 = u.atoms[:n_fw], u.atoms[n_fw:]
L = u.dimensions[:3]

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")
u.trajectory[0]
fwpos = fw.positions.copy()
ax.scatter(fwpos[::3, 0], fwpos[::3, 1], fwpos[::3, 2], s=2, c="lightgray", alpha=0.15)
p0 = co2.positions
sc = ax.scatter(p0[:, 0], p0[:, 1], p0[:, 2], s=55, c="red")
ax.set_xlim(0, L[0]); ax.set_ylim(0, L[1]); ax.set_zlim(0, L[2])
ax.set_title("CO2 diffusing in the %s-zeolite" % label)

frames = range(0, len(u.trajectory), 10)
def update(i):
    u.trajectory[i]
    p = co2.positions
    sc._offsets3d = (p[:, 0], p[:, 1], p[:, 2])
    return sc,

ani = FuncAnimation(fig, update, frames=frames, blit=False)
out = "%s_diffusion.gif" % label
ani.save(out, writer=PillowWriter(fps=15), dpi=80)
print("wrote", out)
