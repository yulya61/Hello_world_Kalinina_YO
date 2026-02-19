files = ["seq1", "seq2", "seq3", "seq4"]
date = "2026-02-19"  # фиксированная дата взятия образца

for name in files:
    new_name = name + "_" + date + ".fasta"
    print(new_name)