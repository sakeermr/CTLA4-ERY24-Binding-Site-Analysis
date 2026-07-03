import os
import subprocess

docker_path = r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'

# Replicates 2, 3, 4 (run_2 was replicate 1)
seeds = [2, 3, 4]

for seed in seeds:
    run_dir = "results/haddock3_run_seed" + str(seed)
    print("="*60)
    print("ENSEMBLE REPLICATE " + str(seed))
    print("="*60)

    config_content = '''run_dir = "''' + run_dir + '''"

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

    config_file = "config/haddock3_rep" + str(seed) + ".cfg"
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

    print("Running replicate " + str(seed) + " (15-30 min)...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
    if result.returncode == 0:
        print("Replicate " + str(seed) + " DONE -> " + run_dir)
    else:
        print("Replicate " + str(seed) + " error:")
        print(result.stdout[-1200:])
        print(result.stderr[-600:])
    print("")

print("All ensemble runs complete.")