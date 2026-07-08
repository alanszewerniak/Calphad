import subprocess
r = subprocess.run(["simulate"], capture_output=True, text=True)
print("RETURN CODE:", r.returncode)
print("---- last stdout ----")
print("\n".join(r.stdout.splitlines()[-12:]))
print("---- last stderr ----")
print("\n".join(r.stderr.splitlines()[-12:]))

#runs the simulation and prints the reason for a crash if there was to be one so i can debug and fix the issue 
