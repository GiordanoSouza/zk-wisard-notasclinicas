#!/usr/bin/env python
"""
Treina um classificador Bloom WiSARD simples.
Salva o modelo em 'model.npz' (bitmaps + metadados).
"""

import argparse, json, pathlib
import numpy as np, pandas as pd
from tqdm import tqdm

def train(bitar: np.ndarray, labels: np.ndarray, n_classes: int):
    """
    Cria um bitmap por classe: OR bit-a-bit das amostras pertencentes à classe.
    """
    M = bitar.shape[1]
    discriminators = np.zeros((n_classes, M), dtype=np.uint8)
    for cls in range(n_classes):
        cls_bits = bitar[labels == cls]
        if len(cls_bits):
            discriminators[cls] = np.bitwise_or.reduce(cls_bits, axis=0)
    return discriminators

def main(bits_file: str, out_model: str):
    df = pd.read_parquet(bits_file)
    bits   = np.stack(df['bits'].to_numpy())
    labels = df['label'].to_numpy()
    n_cls  = len(set(labels))

    model = train(bits, labels, n_cls)
    np.savez(out_model, discriminators=model)
    print(f"✔ Modelo salvo em {out_model}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("bits_file")
    p.add_argument("-o", "--out-model", default="model.npz")
    a = p.parse_args()
    main(a.bits_file, a.out_model)
