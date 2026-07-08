from pymatgen.core import Structure
from collections import deque

# 1. load pure-silica FAU
fau = Structure.from_file("FAU.cif")

# 2. Si-Si neighbour map, two-colour it like a chessboard
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

# 3. turn one colour into Al  ->  Si96 Al96 O384
doped = fau.copy()
for i, c in color.items():
    if c == 1:
        doped.replace(i, "Al")

# 4. read Na positions as a pocket map only
nax = Structure.from_file("NaX.cif")
na_coords = [site.frac_coords for site in nax
             if any(el.symbol == "Na" for el in site.species.elements)]

# 5. pick 48 well-separated positions (Ni is 2+, same count as Fe)
lattice = doped.lattice
min_dist = 3.5
selected = []
for coord in na_coords:
    if len(selected) >= 48:
        break
    if all(lattice.get_distance_and_image(coord, s)[0] >= min_dist for s in selected):
        selected.append(coord)

# 6. add 48 Ni
for coord in selected:
    doped.append("Ni", coord, coords_are_cartesian=False)

# 7. report and save
print("Final composition:",
      "Ni", int(doped.composition["Ni"]),
      " Si", int(doped.composition["Si"]),
      " Al", int(doped.composition["Al"]),
      " O", int(doped.composition["O"]))
print("Charge check (should be 0):",
      int(doped.composition["Ni"]) * 2 - int(doped.composition["Al"]))

doped.to(filename="Ni_zeolite.cif")
print("Saved Ni_zeolite.cif")

#this is the exact same framework as Fe_zeolite.cif, but with 48 Ni2+ ions instead of 48 Fe2+ ions
#within this framework I am setting up the raspa set up and the gromac set up
#with in this set up I will ensure the positions of the zeolite mesh consisting of Si, Al, O and Ni2+ ions
#main focus is to ensure that the ions balance and so that the composition of the zeolite is correct ensuring the ratio of Si:Al is 1:1