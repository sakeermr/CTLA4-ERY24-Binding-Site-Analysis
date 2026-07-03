import os
import subprocess

docker_path = r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'

print("="*60)
print("ERY2-4 TO CTLA-4 DOCKING - HADDOCK3 (AlphaFold peptide)")
print("="*60)

for d in ['config', 'results']:
    if not os.path.exists(d):
        os.makedirs(d)

config_content = '''run_dir = "results/haddock3_run_2"

molecules = [
    "structures/ctla4_A.pdb",
    "structures/ery24_B.pdb"
    ]

[topoaa]

[rigidbody]
ambig_fname = "config/ery24_restraints.tbl"
sampling = 200
crossdock = false

[caprieval]

[seletop]
select = 50

[flexref]
ambig_fname = "config/ery24_restraints.tbl"

[caprieval]

[emref]
ambig_fname = "config/ery24_restraints.tbl"

[caprieval]

[clustfcc]
min_population = 4

[seletopclusts]
top_clusters = 10

[caprieval]
'''

config_file = "config/haddock3_workflow.cfg"
with open(config_file, 'w') as f:
    f.write(config_content)

print("Config created. Starting HADDOCK3...")

work_path = os.path.abspath('.')
cmd = [
    docker_path, 'run', '--rm',
    '-v', work_path + ':/haddock_work',
    '-w', '/haddock_work',
    'haddock3-ery24:latest',
    'haddock3', config_file
]

print("Running HADDOCK3 (15-30 minutes)...")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
print(result.stdout[-3000:])
if result.stderr:
    print("Stderr: " + result.stderr[-1500:])

if result.returncode == 0:
    print("")
    print("SUCCESS! Results in: results/haddock3_run_2")
else:
    print("Return code: " + str(result.returncode))