#!/usr/bin/env python3
"""Remet sur le site toutes les photos de cuisines des envois C-LINE."""
import os, subprocess, shutil

S = '/private/tmp/claude-501/-Users-dreyfus-C-LINE/bfcdd7d9-09a2-40f4-9b9a-bbf5c1a345ee/scratchpad/cl'
DEST = 'site/wp-content/uploads/2026/11'
os.makedirs(DEST, exist_ok=True)

CUISINES = [2,3,6,7,8,9,10,11,13,15,16,18,19,21,22,23,25,26,27,30,31,32,34,35,
            36,37,38,39,40,43,44,45,50,52,54,55,58,59,61,62,63,65,66,67,68,69,70,
            71,72,74,76,77,79,81,83,84,86,88,89,91,92,94,95,97,98,99,102,
            107,108,111,112,113,116,117,118,119,120,124,125,126,127,128,130,132,135,137,138,139,140,
            144,145,146]
SDB = [60, 93, 143]

def installer(nums, prefixe):
    sorties = []
    for i, n in enumerate(nums, 1):
        src = os.path.join(S, 'c%03d.jpeg' % n)
        if not os.path.exists(src):
            print('  absent :', src); continue
        nom = '%s-%03d.jpg' % (prefixe, i)
        subprocess.run(['sips', '-Z', '1500', '-s', 'formatOptions', '80', src,
                        '--out', os.path.join(DEST, nom)], capture_output=True)
        sorties.append('/wp-content/uploads/2026/11/' + nom)
    return sorties

cuisines = installer(CUISINES, 'cuisine')
sdb = installer(SDB, 'sdb')
print('cuisines installees :', len(cuisines))
print('salles de bain      :', len(sdb))

import json
json.dump({'cuisines': cuisines, 'sdb': sdb}, open('/tmp/cline_photos.json', 'w'))
