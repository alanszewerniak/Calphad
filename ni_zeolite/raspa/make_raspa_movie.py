import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import glob, os

D = "Movies/System_0"

def read_pdb_frames(path):
    frames, cur = [], []
    for ln in open(path):
        if ln.startswith(("ATOM", "HETATM")):
            try:
                cur.append((float(ln[30:38]), float(ln[38:46]), float(ln[46:54])))
            except ValueError:
                pass
        elif ln.startswith("ENDMDL"):
            frames.append(cur); cur = []
    if cur:
        frames.append(cur)
    return frames

fw = read_pdb_frames(os.path.join(D, "Framework_0_final.pdb"))[0]
fwx = [p[0] for p in fw]; fwy = [p[1] for p in fw]; fwz = [p[2] for p in fw]

co2_path = glob.glob(os.path.join(D, "*component_CO2_0.pdb"))[0]
co2_frames = read_pdb_frames(co2_path)
print("snapshots:", len(co2_frames))

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")

def update(i):
    ax.clear()
    ax.scatter(fwx, fwy, fwz, s=2, c="lightgray", alpha=0.15)
    f = co2_frames[i]
    if f:
        ax.scatter([p[0] for p in f], [p[1] for p in f], [p[2] for p in f], s=55, c="red")
    ax.set_title("CO2 adsorbed in Ni-zeolite  (GCMC snapshot %d)" % (i + 1))

ani = FuncAnimation(fig, update, frames=len(co2_frames), blit=False)
ani.save("ni_co2_adsorption.gif", writer=PillowWriter(fps=3), dpi=80)
print("wrote ni_co2_adsorption.gif")
