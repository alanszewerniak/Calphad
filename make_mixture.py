import os, shutil
metals = [("Fe", "FeZeoliteFF"), ("Ni", "NiZeoliteFF"), ("Cr", "CrZeoliteFF")]
tmpl = """SimulationType                MonteCarlo
NumberOfCycles                5000
NumberOfInitializationCycles  2000
PrintEvery                    1000

Forcefield                    {ff}
ChargeMethod                  Ewald
CutOff                        12.0
UseChargesFromCIFFile         no

Framework 0
FrameworkName                 {fw}
UnitCells                     1 1 1
ExternalTemperature           298.0
ExternalPressure              1e5

Component 0 MoleculeName             CO2
            MoleculeDefinition       ExampleDefinitions
            MolFraction              0.5
            TranslationProbability   1.0
            RotationProbability      1.0
            ReinsertionProbability   1.0
            SwapProbability          2.0
            CreateNumberOfMolecules  0

Component 1 MoleculeName             methane
            MoleculeDefinition       ExampleDefinitions
            MolFraction              0.5
            TranslationProbability   1.0
            ReinsertionProbability   1.0
            SwapProbability          2.0
            CreateNumberOfMolecules  0
"""
for m, ff in metals:
    base = os.path.expanduser("~/Calphad/%s_zeolite/raspa" % m.lower())
    mix = os.path.join(base, "mix")
    os.makedirs(mix, exist_ok=True)
    shutil.copy(os.path.join(base, "%s_zeolite.cif" % m), mix)
    open(os.path.join(mix, "simulation.input"), "w").write(tmpl.format(ff=ff, fw="%s_zeolite" % m))
    print("wrote", os.path.join(mix, "simulation.input"))
