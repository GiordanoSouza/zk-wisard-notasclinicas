#!/usr/bin/env python
"""
Carrega modelo .npz e gera predições para um Parquet de bits.
"""

import argparse, numpy as np, pandas as pd
from tqdm import tqdm

def predict(discriminators: np.ndarray, bits: np.ndarray):
    # pontuação = soma AND entre bits de entrada e discriminador
    scores = (discriminators & bits).sum(axis=1)
    return int(scores.argmax())

def main(model_file, bits_file, out_csv):
    discr = np.load(model_file)['discriminators']
    df    = pd.read_parquet(bits_file)
    preds = []
    for b in tqdm(df['bits'], desc="Predict"):
        preds.append(predict(discr, b))
    df['pred'] = preds
    df.to_csv(out_csv, index=False)
    print(f"✔ Predições salvas em {out_csv}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("model_file")
    p.add_argument("bits_file")
    p.add_argument("-o", "--out-csv", default="predictions.csv")
    a = p.parse_args()
    main(a.model_file, a.bits_file, a.out_csv)
