import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# CO2 and CH4 loadings (mol/kg) from equimolar 50/50 mixture GCMC, 298 K, 1 bar
data = {"Fe": (4.2396, 0.0626), "Ni": (4.2676, 0.0713), "Cr": (5.3452, 0.0429)}
labels = ["Fe", "Ni", "Cr"]
colors = {"Fe": "indianred", "Ni": "steelblue", "Cr": "seagreen"}
sel = [data[m][0] / data[m][1] for m in labels]

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(labels, sel, color=[colors[m] for m in labels], edgecolor="k", linewidth=0.6)
ax.set_ylabel("CO$_2$ / CH$_4$ selectivity", fontsize=11)
ax.set_title("CO$_2$/CH$_4$ selectivity of doped FAU zeolite\nequimolar mixture GCMC,  298 K,  1 bar", fontsize=13, weight="bold")
for b, v in zip(bars, sel):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, "%.0f" % v, ha="center", fontsize=11, weight="bold")
ax.set_ylim(0, 145)
ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "Selectivity = CO2 loading / CH4 loading for a 50/50 feed. Cr is a shorter run, so its value is more approximate.",
         ha="center", fontsize=8, color="0.35")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("selectivity_comparison.png", dpi=150)
print("wrote selectivity_comparison.png  ->", {m: round(s) for m, s in zip(labels, sel)})
