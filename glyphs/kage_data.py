
from os import path

filepath = path.join(path.dirname(__file__), '..', 'kage.tsv')

def load():
    kage_data = {}
    with open(filepath, 'r') as f:
        for line in f:
            entries = line.strip().split('\t')
            if len(entries) != 3:
                continue
            name, related, data = entries
            kage_data[name] = data
    return kage_data
