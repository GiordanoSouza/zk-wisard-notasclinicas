# ZK-WiSARD Clinical Text Classification

Protótipo de **classificação sigilosa** de textos clínicos usando uma rede
**Bloom WiSARD** (weightless neural network) combinada a **provas de conhecimento
zero** (ZKP) em Circom/Groth16.

## Visão Geral

1. **`scripts/preprocessing/encode_bits.py`**  
   Converte notas clínicas em vetores fixos de bits por meio de tokenização +
   funções de hash (Bloom filter).

2. **`scripts/wisard`**  
   - `train_model.py` treina a Bloom WiSARD.  
   - `predict.py` carrega o modelo treinado e gera predições.

3. **`scripts/zk`**  
   - `build_witness.py` gera `witness.json` (bits + classe esperada).  
   - `verify_proof.py` demonstra, de ponta-a-ponta, como compilar o circuito,
     fazer o trusted setup, gerar e verificar a prova ZK usando SnarkJS.

4. **`circuits/circom/wisard.circom`**  
   Circuito Circom minimalista que executa o arg-max de pontuações por classe e
   comprova que a classe resultante coincide com a pública (`expected`).

## Como rodar (resumo)

```bash
# Pré-processa e treina
python scripts/preprocessing/encode_bits.py data/raw/mtsamples.csv
python scripts/wisard/train_model.py data/processed/bits.parquet

# Gera witness da 1ᵃ amostra
python scripts/zk/build_witness.py \
       --bits-file data/processed/bits.parquet --index 0

# Compila - setup - prova - verificação
bash scripts/zk/verify_proof.ps1
