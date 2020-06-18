from datetime import datetime as dt
from glob import glob
from pathlib import Path
from sys import stderr

from udar import Document
from udar import ALL

CORPUS_GLOB = '/path/to/repo/corpus/*.txt'
LEVELS = {'A1', 'A2', 'B1', 'B2', 'C1', 'C2'}
output_filename = 'udar_features.tsv'


def level_from_filename(filename):
    p = Path(filename)
    level = p.name.split('_')[0]
    assert level in LEVELS, f'{level} is an invalid level.'
    return level


filenames = glob(CORPUS_GLOB)
# redo = input(f'Process files already in {output_filename}? (Y/n) ')
redo = 'y'
if redo in {'y', 'Y', ''}:
    already_done = set()
    with open(output_filename, 'w') as f:
        print('filename', *ALL._get_cat_and_feat_names(), 'tot_seconds',
              'level', sep='\t', file=f)
else:
    try:
        with open(output_filename) as f:
            already_done = {line.split('\t')[0] for line in f}
    except FileNotFoundError:
        already_done = set()
filenames = [fname for fname in filenames if fname not in already_done]

fname_dict = {level: [] for level in LEVELS}
fname_dict['??'] = []
for fname in filenames:
    fname_dict[level_from_filename(fname)].append(fname)
del fname_dict['??']

with open(output_filename, 'a') as output_file:
    while any(fname_dict.values()):
        for level, level_fnames in sorted(fname_dict.items()):
            if level_fnames:
                filename = level_fnames.pop()
                t1 = dt.now()
                print(f'processing {filename} ...', file=stderr, flush=True)
                print(f'\t{level}', file=stderr, flush=True)
                with open(filename) as f:
                    print('\tmaking document...', file=stderr, flush=True)
                    doc = Document(f.read(), disambiguate=True, depparse=True)
                print('\textracting features...', file=stderr, flush=True)
                features = ALL(doc)
                t2 = dt.now()
                elapsed = (t2 - t1).total_seconds()
                print(filename, *features[1], elapsed, level, sep='\t',
                      file=output_file, flush=True)
