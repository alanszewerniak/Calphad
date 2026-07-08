import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# uptake, mol/kg framework (GCMC, 298 K, 1 bar)
up_labels = ["Silica\n(baseline)", "Ni", "Fe", "Cr"]
up_vals   = [0.56, 5.07, 5.11, 6.16]
up_err    = [0.0, 0.27, 0.27, 0.16]
up_colors = ["0.7", "steelblue", "indianred", "seagreen"]

# diffusion, 1e-5 cm^2/s (MD, 298 K)
df_labels = ["Ni", "Fe", "Cr"]
df_vals   = [0.0348, 0.0186, 0.0114]
df_err    = [0.06, 0.03, 0.02]
df_colors = ["steelblue", "indianred", "seagreen"]

# ---- uptake chart ----
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(up_labels, up_vals, yerr=up_err, capsize=6, color=up_colors,
              edgecolor="k", linewidth=0.6)
ax.set_ylabel("CO$_2$ uptake  (mol per kg framework)", fontsize=11)
ax.set_title("CO$_2$ uptake in doped FAU zeolite\nGCMC,  298 K,  1 bar", fontsize=13, weight="bold")
for b, v in zip(bars, up_vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.15, "%.2f" % v, ha="center", fontsize=10)
ax.set_ylim(0, 7); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("uptake_comparison.png", dpi=150)
print("wrote uptake_comparison.png")

# ---- diffusion chart ----
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(df_labels, df_vals, yerr=df_err, capsize=6, color=df_colors,
              edgecolor="k", linewidth=0.6)
ax.set_ylabel("Self-diffusion coefficient D  (1e-5 cm$^2$/s)", fontsize=11)
ax.set_title("CO$_2$ diffusion in doped FAU zeolite\nMD,  298 K,  500 ps", fontsize=13, weight="bold")
for b, v in zip(bars, df_vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.001, "%.4f" % v, ha="center", fontsize=10)
ax.set_ylim(0, 0.11); ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "Note: error bars exceed the values, so this ordering is indicative only.",
         ha="center", fontsize=8, color="0.35")
fig.tight_layout(rect=[0, 0.04, 1, 1]); fig.savefig("diffusion_comparison.png", dpi=150)
print("wrote diffusion_comparison.png")
