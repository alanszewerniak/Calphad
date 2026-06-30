# RASPA CO2 Adsorption: What I Did, Explained

A short reference of the RASPA side of the Fe-zeolite project, with the code and the fine details that actually mattered.

## What RASPA does
RASPA runs Grand Canonical Monte Carlo (GCMC). It does not move molecules through time. It repeatedly tries to insert, delete and jump CO2 molecules at random and accepts or rejects each move by an energy rule, until it has a statistically representative picture of how much CO2 the framework holds at a set temperature and pressure. The headline output is the loading (CO2 per gram of framework). True motion through time is molecular dynamics, which is the GROMACS job.

## 1. Installing RASPA (it has no Windows build)
RASPA only builds on Linux, so it runs inside WSL (Windows Subsystem for Linux).

    wsl --install            # in admin PowerShell, then restart
    # inside Ubuntu:
    bash Miniconda3-latest-Linux-x86_64.sh   # install conda
    conda install -c conda-forge raspa2      # the Linux build exists

- The RASPA program is called `simulate`.
- Its data (force fields, molecule models, example structures) lives in `/home/alan/miniconda3/share/raspa/`.
- RASPA finds that data through an environment variable, set once in `~/.bashrc`:

      export RASPA_DIR=/home/alan/miniconda3

Fine detail: if a download says "could not resolve host", WSL is using a stale DNS after a network change. Fix with `wsl --shutdown` in Windows PowerShell, then reopen Ubuntu.

## 2. A force field is just two text files
A force field tells RASPA how atoms interact. My force field folder `FeZeoliteFF` holds two files:

- `force_field_mixing_rules.def` = the Lennard-Jones values (epsilon, sigma) for every atom type. Epsilon in Kelvin, sigma in Angstroms. This is the short-range push and pull between atoms.
- `pseudo_atoms.def` = the identity and the charge of every atom type. The charge column drives the electrostatics, which is what actually pulls CO2 onto the Fe.

Fine detail: RASPA only looks for a named force field inside `$RASPA_DIR/share/raspa/forcefield/`, NOT in your working folder. So after editing the files I had to copy them back there:

    cp FeZeoliteFF/pseudo_atoms.def FeZeoliteFF/force_field_mixing_rules.def \
       /home/alan/miniconda3/share/raspa/forcefield/FeZeoliteFF/

### The Fe Lennard-Jones line
RASPA already shipped an Fe value (UFF) in its MOF force field, so I reused it rather than inventing one:

    Fe_   lennard-jones   6.54185   2.5943   // UFF

Fine detail: the mixing-rules file has a count line saying how many interactions are defined. Adding an atom means bumping that number by one.

### The charges
The example zeolite force field is for neutral all-silica zeolites, so it carries little charge. My system is electrostatic (negative Al sites, Fe2+ pulling on CO2), so I needed real charges. I took the framework charges from a paper on GCMC of CO2 in 13X (Chen et al. 2018), the same framework and method:

    O = -0.359,  Si = +0.26,  Al = +0.713

Fe was not in that paper, so I set its charge by the rule that the whole cell must be electrically neutral. Framework total over my structure was -44.45, spread over 48 Fe, giving:

    Fe = +0.93

Fine detail: `pseudo_atoms.def` is parsed strictly by the count, so it must have NO blank lines between entries, or RASPA loses track of the atoms.

## 3. The structure file and the label trap
The framework is `Fe_zeolite.cif`. RASPA reads the second column of the atom list, the `_atom_site_label`. My cif, written by pymatgen, had labels like `T1` and `Al48` instead of element names, so RASPA could not match them to the force field and gave every framework atom NO van der Waals interaction. The result was meaningless (it came out below bare silica).

The fix had two halves:
- Relabel every atom in the cif so the label equals its element (Si, Al, O, Fe).
- Rename the force-field atoms from `Si_, O_, Al_, Fe_` to bare `Si, O, Al, Fe` so they match.

Both done with short Python one-liners (avoiding `$`, hyphens and regex, which kept getting corrupted on paste into the terminal).

Fine detail: how to tell the run was now correct is `grep -c "NO VDW"` on the output returning 0.

## 4. The control file: simulation.input
This tells RASPA what run to do. Mine, with explanations:

    SimulationType                MonteCarlo      # GCMC, not MD
    NumberOfCycles                5000            # production sampling
    NumberOfInitializationCycles  2000            # warm-up, discarded
    PrintEvery                    1000

    Forcefield                    FeZeoliteFF     # my force field folder
    ChargeMethod                  Ewald           # electrostatics on (needed for the Fe)
    CutOff                        12.0            # LJ cutoff in Angstroms
    UseChargesFromCIFFile         no              # use the charges in pseudo_atoms.def

    Framework 0
    FrameworkName                 Fe_zeolite      # loads Fe_zeolite.cif
    UnitCells                     1 1 1
    ExternalTemperature           298.0           # 25 C
    ExternalPressure              1e5             # 1 bar

    Component 0 MoleculeName             CO2
                MoleculeDefinition       ExampleDefinitions   # the TraPPE CO2 model
                TranslationProbability   1.0
                RotationProbability      1.0
                ReinsertionProbability   1.0
                SwapProbability          2.0     # the insert/delete moves = the GCMC
                CreateNumberOfMolecules  0       # start empty, let it fill

Fine detail: `ChargeMethod Ewald` is what switches the electrostatics on. Without it the Fe-CO2 attraction, the whole point, is missing.

## 5. Running it and reading the result
    simulate

Output lands in `Output/System_0/output_Fe_zeolite_..._.data`. Pull the uptake with:

    grep -i "loading absolute" Output/System_0/output_Fe_zeolite_*.data

My result: 5.11 mol/kg (about 225 mg/g) at 298 K, 1 bar, against a bare-silica baseline of 0.56 mol/kg. So the Fe roughly nine-folded the CO2 uptake, exactly the electrostatic-binding mechanism, and the value sits in the realistic range for real cation-exchanged X zeolites (4 to 5 mmol/g).

Fine detail: with Ewald on, the run is much slower than the chargeless silica test, so be patient and wait for the prompt to return.

## The gotchas, in one place
1. RASPA only finds force fields in `$RASPA_DIR/share/raspa/forcefield/`, not the local folder.
2. `pseudo_atoms.def` breaks if there are blank lines between entries.
3. The cif `_atom_site_label` must match the force-field atom names, or you get NO VDW and a junk result.
4. `ChargeMethod Ewald` must be on, or the electrostatics, the entire Fe effect, are off.
5. The Fe charge (+0.93) is set by overall neutrality, an assumption to state, ideally replaced later by DFT charges.
6. The loading is only valid once `grep -c "NO VDW"` returns 0.
