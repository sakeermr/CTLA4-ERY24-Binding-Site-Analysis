import numpy as np
from Bio.PDB import PDBParser

def dist(a, b):
    return np.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

b7_site = [33, 35, 53, 63, 65, 95, 97, 99, 100, 101, 102, 103, 104, 105, 106]
guided_site = [95, 97, 98, 99, 100, 102, 103, 104, 105, 106]
blind_site  = [16, 61, 62, 63, 64, 65, 66, 68, 69, 70, 82, 127]

parser = PDBParser(QUIET=True)
st = parser.get_structure('ctla4', 'structures/ctla4_A.pdb')[0]
chainA = st['A']

def ca_coords(reslist):
    coords = {}
    for r in chainA.get_residues():
        if r.get_id()[1] in reslist and 'CA' in r:
            coords[r.get_id()[1]] = r['CA'].coord
    return coords

b7_ca = ca_coords(b7_site)

def min_dist_to_b7(site):
    site_ca = ca_coords(site)
    dmin = 999.0
    closest = None
    for rs, cs in site_ca.items():
        for rb, cb in b7_ca.items():
            d = dist(cs, cb)
            if d < dmin:
                dmin = d
                closest = (rs, rb)
    return dmin, closest, len(site_ca)

print('='*60)
print('TIEBREAKER: which site can explain B7-1 competition?')
print('='*60)
print('')
print('Known fact: ERY2-4 competitively inhibits B7-1 (IC50 ~1.1 uM)')
print('B7-1 binds CTLA-4 at:', b7_site)
print('')

for name, site in [('GUIDED site (95-106)', guided_site), ('BLIND site (61-70)', blind_site)]:
    overlap = sorted(set(site) & set(b7_site))
    dmin, closest, n = min_dist_to_b7(site)
    print(name + ':')
    print('  Direct overlap with B7-1: ' + str(len(overlap)) + ' residues ' + str(overlap))
    print('  Closest approach to B7-1: ' + str(round(dmin,1)) + ' A (res ' + str(closest[0]) + ' <-> B7-res ' + str(closest[1]) + ')')
    if len(overlap) >= 5:
        verdict = 'DIRECT STERIC BLOCK - fully explains competition'
    elif dmin < 10:
        verdict = 'ADJACENT - could partially occlude B7-1'
    else:
        verdict = 'DISTANT - cannot easily explain competition'
    print('  --> ' + verdict)
    print('')

print('='*60)
print('A site overlapping/abutting B7-1 is consistent with the')
print('experimental competition. A distant site would require an')
print('allosteric mechanism - a much stronger, less likely claim.')
print('='*60)
