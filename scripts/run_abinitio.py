import os
import subprocess

docker_path = r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'

print("="*60)
print("AB-INITIO (blind) DOCKING - no guiding restraints")
print("="*60)

config_content = '''run_dir = "results/haddock3_abinitio"

molecules = [
    "structures/ctla4_A.pdb",
    "structures/ery24_B.pdb"
    ]

[topoaa]

[rigidbody]
sampling = 1000
crossdock = false
ranair = true

[caprieval]

[seletop]
select = 200

[flexref]

[caprieval]

[emref]

[caprieval]

[clustfcc]
min_population = 4

[seletopclusts]
top_clusters = 10

[caprieval]
'''

config_file = "config/haddock3_abinitio.cfg"
with open(config_file, 'w') as f:
    f.write(config_content)

work_path = os.path.abspath('.')
cmd = [
    docker_path, 'run', '--rm',
    '-v', work_path + ':/haddock_work',
    '-w', '/haddock_work',
    'haddock3-ery24:latest',
    'haddock3', config_file
]

print("Running blind docking (1000 models - this takes LONGER,")
print("roughly 45-90 min). Let it run.")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=14400)
tail = result.stdout[-2000:] if result.stdout else ""
print(tail)
if result.returncode == 0:
    print("")
    print("SUCCESS -> results/haddock3_abinitio")
else:
    print("Return code: " + str(result.returncode))
    if result.stderr:
        print(result.stderr[-800:])