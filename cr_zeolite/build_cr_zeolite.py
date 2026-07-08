from pymatgen.core import Structure
from collections import deque

fau = Structure.from_file("FAU.cif")

neighbors = fau.get_all_neighbors(3.5)
adj = {}
for i, site in enumerate(fau):
    if site.species_string == "Si":
        adj[i] = [n.index for n in neighbors[i] if fau[n.index].species_string == "Si"]

color = {}
for start in adj:
    if start in color:
        continue
    color[start] = 0
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if nb not in color:
                color[nb] = 1 - color[node]
                queue.append(nb)

doped = fau.copy()
for i, c in color.items():
    if c == 1:
        doped.replace(i, "Al")

nax = Structure.from_file("NaX.cif")
na_coords = [site.frac_coords for site in nax
             if any(el.symbol == "Na" for el in site.species.elements)]

lattice = doped.lattice
min_dist = 3.5
selected = []
for coord in na_coords:
    if len(selected) >= 32:
        break
    if all(lattice.get_distance_and_image(coord, s)[0] >= min_dist for s in selected):
        selected.append(coord)

for coord in selected:
    doped.append("Cr", coord, coords_are_cartesian=False)

print("Final composition:",
      "Cr", int(doped.composition["Cr"]),
      " Si", int(doped.composition["Si"]),
      " Al", int(doped.composition["Al"]),
      " O", int(doped.composition["O"]))
print("Charge check (should be 0):",
      int(doped.composition["Cr"]) * 3 - int(doped.composition["Al"]))

doped.to(filename="Cr_zeolite.cif")
print("Saved Cr_zeolite.cif")
