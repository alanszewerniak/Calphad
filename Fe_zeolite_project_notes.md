# Fe-Zeolite CO2 Capture Project — Working Notes

Last updated: 30 June 2026

## What this project is
Computational study of transition-metal-doped zeolites for CO2 capture, screening Fe, then Ni, then Cr as individual single-metal dopants in the FAU (faujasite / 13X) framework. Pair strand to the Fe-Cr-Ni alloy/CALPHAD work.
Contribution: carbon capture and decarbonisation (the energy transition), not renewable energy generation. Lead with the CO2 capture angle; natural-gas sweetening is a secondary, fossil-fuel application.

Workflow: ASE/pymatgen builds the structure, RASPA2 does the CO2 adsorption (GCMC), GROMACS does the diffusion (MD).

## Status
- Structure: DONE. Fe_zeolite.cif built, charge-balanced.
- RASPA2: INSTALLED and configured in WSL.
- RASPA validation run: DONE on pure-silica FAU (worked).
- Force field: Fe Lennard-Jones DONE. Charges = the last remaining piece (now sourced, see below).

## The structure (recap of how it was built)
Base framework: idealised all-silica FAU.cif from the IZA Structure Database (576 atoms = 192 Si + 384 O).
Build pipeline (script: build_fe_zeolite.py):
1. Load FAU.cif.
2. Build Si-Si neighbour map, two-colour it like a chessboard (neighbours opposite colours).
3. Turn one colour into Al -> alternating Si/Al, obeys Lowenstein (no Al-O-Al). Gives Si96 Al96 O384, Si:Al = 1.
4. Read Na cation positions from NaX.cif (IZA, Na-X dehydrated) as a position guide only (Na never converted, just a map of pocket locations).
5. Pick 48 well-separated positions (min 3.5 A apart) for the Fe.
6. Add 48 Fe -> Fe48 Si96 Al96 O384, net charge 0.
Charge logic: each Al = -1, each Fe2+ = +2, so 96 Al need 48 Fe (one Fe per two Al).

## RASPA install (so it can be redone / used for GROMACS)
RASPA has no Windows build, so it runs inside WSL (Windows Subsystem for Linux).
- Installed WSL + Ubuntu (wsl --install in admin PowerShell; needed a restart).
- Installed Miniconda inside Ubuntu.
- conda install -c conda-forge raspa2  (Linux build exists).
- RASPA program is called: simulate
- RASPA data lives in: /home/alan/miniconda3/share/raspa/
- Set environment variable (in ~/.bashrc): export RASPA_DIR=/home/alan/miniconda3
- WSL DNS tip: if downloads/git "cannot resolve host", run wsl --shutdown in Windows PowerShell, reopen Ubuntu (refreshes DNS after a network change).
GROMACS will install the same way later (conda, it is also Linux-native).

## Validation run result (baseline to beat)
Pure-silica FAU, CO2, 298 K, 1 bar:
- ~6.4 CO2 molecules per unit cell = 0.56 mol/kg = ~24 mg/g.
Sensible for bare silica. The Fe version should hold more, because Fe2+ adds electrostatic binding that pure silica lacks. This 0.56 mol/kg is the number the Fe result should exceed.

## Force field
Working copy: ~/Calphad/fe_zeolite/raspa/FeZeoliteFF (copied from ExampleZeolitesForceField).
Two files: force_field_mixing_rules.def (Lennard-Jones) and pseudo_atoms.def (identity + charge).

### DONE: Fe Lennard-Jones
Added to force_field_mixing_rules.def (taken from RASPA's ExampleMOFsForceField, UFF):
  Fe_   lennard-jones   6.54185   2.5943   // UFF
(epsilon in K, sigma in A). Remember to bump the "number of interactions" count when adding atoms.

### TO DO: charges (and a consistent framework Lennard-Jones)
Source found: Chen, Zhu, Tang, Fu, Li, Xiao (2018), "Molecular simulation and experimental investigation of CO2 capture in 13X zeolite". This is FAU/13X (our framework) using GCMC + UFF + Ewald + Lorentz-Berthelot + 12 A cutoff (matches RASPA). It gives a complete, consistent, citable force field.

Framework partial charges (Chen 2018, Table 1), in e:
  O = -0.359,  Si = +0.26,  Al = +0.713,  Na = +0.57
CO2 charges: C = +0.72, O = -0.36.

Lennard-Jones (Chen 2018, Table 2, UFF): sigma in A, epsilon in kJ/mol -> converted to K for RASPA (divide kJ/mol by 0.0083145). DOUBLE-CHECK these conversions before use:
  atom   sigma(A)   eps(kJ/mol)   eps(K, for RASPA)
  O       3.500       0.251          ~30.2
  C       3.851       0.4393         ~52.8
  N       3.660       0.2887         ~34.7
  Si      4.295       1.682          ~202.3
  Al      4.499       2.1129         ~254.1
  Na      2.983       0.1255         ~15.1
  Fe      2.5943      0.0544         6.54185  (UFF, already added)

### The Fe charge (the one thing Chen does not give — Fe not in that paper)
Chen's charges are scaled (Na is +0.57, not formal +1). Each Fe replaces two Na, so a clean, neutral-preserving choice is:
  Fe charge = 2 x Na charge = 2 x 0.57 = +1.14 e
Flag this as a justified first-model assumption. Rigorous version = DFT-derived charges (e.g. DDEC6) on the Fe structure.

## Next steps (resume here)
1. Edit pseudo_atoms.def in FeZeoliteFF: add Fe (mass 55.845, charge +1.14), and set Si/Al/O charges from Chen 2018. Make sure the whole cell sums to neutral.
2. For consistency, update the framework Lennard-Jones in force_field_mixing_rules.def to the Chen/UFF values above (currently it uses the chargeless Bai/Siepmann silica values). Decide whether to keep RASPA's built-in TraPPE CO2 or use Chen's UFF CO2 — keep it consistent either way.
3. Make sure electrostatics is on in simulation.input (ChargeMethod Ewald). Point Forcefield at FeZeoliteFF and FrameworkName at Fe_zeolite.
4. Run simulate. Compare the Fe CO2 uptake against the 0.56 mol/kg silica baseline and against experimental divalent-cation 13X data (e.g. the Mg/Ca/Sr/Ba 13X paper) as a sanity check.

## CURRENT BLOCKER: atom-label mismatch (run completes but result invalid)
What is set up and working:
- Force field FeZeoliteFF copied to $RASPA_DIR/share/raspa/forcefield/ (RASPA only looks there, not the local folder).
- pseudo_atoms.def has 17 atoms incl O_/Si_/Al_/Fe_ with charges. NOTE: must have NO blank lines between entries (the strict count-based parser breaks on blanks).
- Fe_zeolite.cif copied into the run folder. simulation.input points at FeZeoliteFF + Fe_zeolite + ChargeMethod Ewald.

The bug:
- Fe run completes but gives 0.21 mol/kg, BELOW the silica baseline. Invalid.
- RASPA warning: "ATOM-PAIRS WITH NO VDW INTERACTION" listing framework atoms as T1, Al48, Al49...
- Cause: pymatgen labelled the cif atoms (e.g. Al48, T1) but the force field is named Si_/O_/Al_/Fe_. RASPA cannot match them, so framework atoms get NO Lennard-Jones. Also "Number of Cations: 0" (Fe treated as framework, not mobile cation).

The fix (two routes, reconcile cif labels with force-field names):
- Route A: rename the four framework atoms in BOTH pseudo_atoms.def and force_field_mixing_rules.def from Si_/O_/Al_/Fe_ to bare Si/O/Al/Fe, then add `RemoveAtomNumberCodeFromLabel yes` to simulation.input so Al48 -> Al etc.
- Route B: relabel the atoms inside Fe_zeolite.cif to match the force field.
- First check the cif atom-site labels (what is "T1"?) before choosing. After any FF edit, re-copy FeZeoliteFF to $RASPA_DIR.

## Cr and Ni (later, small top-ups)
Same force field, just add each metal's lines. For each metal:
- Its UFF Lennard-Jones (look up / grep RASPA's force fields like the Fe one).
- Its charge and oxidation state. This also changes the cation COUNT via charge balance: Ni2+ -> 48 cations (like Fe2+); Cr3+ -> 32 cations (96 Al / 3). Rebuild the structure with the right count using the same pipeline.
One force field holds Fe, Cr and Ni together; RASPA only uses the parameters for atoms present in the loaded structure.

## GROMACS (diffusion strand, later)
Same parameter VALUES, but GROMACS uses different files and units (epsilon in kJ/mol, sigma in nm; charges unchanged). Match cutoff and combining rule so RASPA and GROMACS describe the same system.

## GitHub
Repo cloned to WSL at ~/Calphad. Work committed there. Push needs a GitHub Personal Access Token (account was locked from password attempts; recover via GitHub, do not hammer it). .gitignore excludes RASPA Output/Movies/Restart/VTK folders.

## Honesty flags to remember
- Fe +1.14 charge is an assumption, justify or replace with DFT.
- Converted epsilon (K) values above are my arithmetic; verify them.
- Treating Fe2+ like a divalent main-group cation ignores its d-electron chemistry; fine for a first model, state it.
- Be ready to defend at interview: what a zeolite is, the sigma phase, what GCMC/RASPA and MD/GROMACS actually do, and why doping with Fe helps.
