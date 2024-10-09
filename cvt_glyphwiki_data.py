
with open('dump_newest_only.txt', 'r') as f, open('kage.tsv', 'w') as out:
    lines = 0
    for line in f:
        lines += 1
        if lines <= 2:
            continue
        entries = line.split('|')
        entries = [entry.strip() for entry in entries]
        if len(entries) == 3:
            out.write('\t'.join(entries) + '\n')
