# Circuito `wisard.circom`

Implementa a lógica *mínima* para provar que um vetor de bits (privado)
classifica-se na mesma especialidade (`expected`) que o modelo Bloom-WiSARD
gera internamente.

## Como compilar e gerar provas

```bash
# 1. No projeto, instale dependências (node >= 18)
npm install -g circom snarkjs

# 2. Compile circuito + WASM
circom wisard.circom --r1cs --wasm --sym

# 3. Faça o trusted setup (Groth16)
snarkjs groth16 setup wisard.r1cs pot12_final.ptau wisard_0000.zkey
snarkjs zkey contribute wisard_0000.zkey wisard_final.zkey -n="first"

# 4. Gere witness
node wisard_js/generate_witness.js wisard_js/wisard.wasm witness.json witness.wtns

# 5. Prove e verifique
snarkjs groth16 prove wisard_final.zkey witness.wtns proof.json public.json
snarkjs groth16 verify verification_key.json public.json proof.json
