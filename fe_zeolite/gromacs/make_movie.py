import MDAnalysis as mda
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

u = mda.Universe("system.gro", "md.xtc")

#loads two things together: the gro gives the atom list and their identities, 
#the xtc gives their positions at every saved moment in the run.

n_fw = 624
fw = u.atoms[:n_fw]
co2 = u.atoms[n_fw:]
L = u.dimensions[:3]

#n_fw is the number of framework atoms
#fw is the framework atoms, CO2 is the rest of the atoms, L is the box size in x,y,z

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")

u.trajectory[0]
fwpos = fw.positions.copy()
ax.scatter(fwpos[::3, 0], fwpos[::3, 1], fwpos[::3, 2], s=2, c="lightgray", alpha=0.15)

p0 = co2.positions
sc = ax.scatter(p0[:, 0], p0[:, 1], p0[:, 2], s=55, c="red")

ax.set_xlim(0, L[0]); ax.set_ylim(0, L[1]); ax.set_zlim(0, L[2])
ax.set_title("CO2 diffusing in the Fe-zeolite")

#the 3D framework is drawn in light gray, the CO2 molecules are drawn in red
#the animation is made by updating the red points to the new positions of the CO2 molecules at each frame of trajectiry

frames = range(0, len(u.trajectory), 10)

#takes a snapshot of the CO2 positions at every 5th frame of the trajectory

def update(i):
    u.trajectory[i]
    p = co2.positions
    sc._offsets3d = (p[:, 0], p[:, 1], p[:, 2])
    return sc,

#update is the function that will be called for each frame of the animation

ani = FuncAnimation(fig, update, frames=frames, blit=False)
ani.save("co2_diffusion.gif", writer=PillowWriter(fps=15),
         dpi=80, progress_callback=lambda i, n: print("frame", i, "of", n))
print("wrote co2_diffusion.gif")

#FuncAnimation runs that update over every chosen frame and PillowWriter saves the sequence as co2_diffusion.gif at 20 frames per second.
#The end result is the framework sitting still in grey while the red CO2 hop and drift through the pores, which is your diffusion made visible.
