#!/usr/bin/env python
"""
Gera 'witness.json' para SnarkJS a partir de um arquivo Parquet de bits.
"""

import argparse, json, pandas as pd

def main(bits_file, index, out_json):
    df = pd.read_parquet(bits_file)
    row = df.iloc[index]
    witness = {
        "inBits":    row['bits'].tolist(),
        "expected":  int(row['label'])
    }
    with open(out_json, 'w') as f:
        json.dump(witness, f, indent=2)
    print(f"✔ Witness salvo em {out_json}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--bits-file", required=True)
    p.add_argument("--index", type=int, default=0, help="linha da amostra")
    p.add_argument("-o", "--out-json", default="witness.json")
    a = p.parse_args()
    main(a.bits_file, a.index, a.out_json)
