import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# CO2 and CH4 loadings (mol/kg) with RASPA statistical spread; equimolar 50/50 GCMC, 298 K, 1 bar
data = {
    "Fe": ((4.2396, 0.1345), (0.0626, 0.0047)),
    "Ni": ((4.2676, 0.1310), (0.0713, 0.0142)),
    "Cr": ((5.3452, 0.1277), (0.0429, 0.0109)),
}
labels = ["Fe", "Ni", "Cr"]
colors = {"Fe": "indianred", "Ni": "steelblue", "Cr": "seagreen"}
sel, err = [], []
for m in labels:
    (c, dc), (h, dh) = data[m]
    s = c / h
    sel.append(s); err.append(s * np.sqrt((dc/c)**2 + (dh/h)**2))

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(labels, sel, yerr=err, capsize=6, color=[colors[m] for m in labels], edgecolor="k", linewidth=0.6)
ax.set_ylabel("CO$_2$ / CH$_4$ selectivity", fontsize=11)
ax.set_title("CO$_2$/CH$_4$ selectivity of doped FAU zeolite\nequimolar mixture GCMC,  298 K,  1 bar", fontsize=13, weight="bold")
for b, v, e in zip(bars, sel, err):
    ax.text(b.get_x() + b.get_width()/2, v + e + 3, "%.0f" % v, ha="center", fontsize=11, weight="bold")
ax.set_ylim(0, 175)
ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "Error bars propagated from the RASPA spread on both loadings. Cr was a shorter run, so its bar is least converged.",
         ha="center", fontsize=8, color="0.35")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("selectivity_comparison.png", dpi=150)
print("wrote selectivity_comparison.png")
