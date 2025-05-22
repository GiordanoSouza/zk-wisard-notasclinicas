#!/usr/bin/env python
"""
Converte textos clínicos em vetores de bits (Bloom filter) e
salva um arquivo Parquet com:
    - bits  : numpy.ndarray (uint8, shape=(M,))
    - label : int
"""

import argparse, hashlib, json, pathlib
from typing import List
import numpy as np
import pandas as pd
from tqdm import tqdm

M           = 1024   # tamanho do vetor de bits
NUM_HASHES  = 3      # k funções de hash

def tokenize(text: str) -> List[str]:
    return text.lower().split()

def make_hash_functions(k: int):
    funcs = []
    for salt in range(k):
        def _h(tok, s=salt):
            h = hashlib.sha256(f"{tok}{s}".encode()).hexdigest()
            return int(h, 16)
        funcs.append(_h)
    return funcs

HASH_FUNCS = make_hash_functions(NUM_HASHES)

def text_to_bits(text: str) -> np.ndarray:
    bits = np.zeros(M, dtype=np.uint8)
    for tok in tokenize(text):
        for h in HASH_FUNCS:
            bits[h(tok) % M] = 1
    return bits

def main(csv_file: str, out_parquet: str):
    df = pd.read_csv(csv_file)
    df = df[['transcription', 'medical_specialty']].dropna().reset_index(drop=True)

    # mapeia especialidades para ints
    labels = sorted(df['medical_specialty'].unique())
    label2int = {lab: i for i, lab in enumerate(labels)}

    rows = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Encoding"):
        bits = text_to_bits(row['transcription'])
        rows.append({'bits': bits, 'label': label2int[row['medical_specialty']]})

    pd.DataFrame(rows).to_parquet(out_parquet, index=False)
    # salva mapping
    mapping_file = pathlib.Path(out_parquet).with_suffix('.labels.json')
    mapping_file.write_text(json.dumps(label2int, indent=2))
    print(f"✔ Saved bits → {out_parquet}")
    print(f"✔ Saved label map → {mapping_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file",  help="CSV cru (mtsamples etc.)")
    parser.add_argument("-o", "--out-parquet", default="data/processed/bits.parquet")
    args = parser.parse_args()
    pathlib.Path(args.out_parquet).parent.mkdir(parents=True, exist_ok=True)
    main(args.csv_file, args.out_parquet)
