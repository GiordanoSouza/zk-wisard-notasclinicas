Param(
    [string]$CircuitFile     = "circuits\circom\wisard.circom",
    [string]$PtauFile        = "powersOfTau28_hez_final_12.ptau",
    [string]$Zkey0           = "wisard_0000.zkey",
    [string]$ZkeyFinal       = "wisard_final.zkey",
    [string]$VerificationKey = "verification_key.json",
    [string]$WitnessJson     = "witness.json",
    [string]$WitnessWtn      = "witness.wtns",
    [string]$ProofJson       = "proof.json",
    [string]$PublicJson      = "public.json"
)

Write-Host "1) Compilando circuito..."
circom $CircuitFile --r1cs --wasm --sym -o circuits\circom

if (-Not (Test-Path $PtauFile)) {
    Write-Host "2) Baixando PTAU..."
    Invoke-WebRequest `
      "https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_12.ptau" `
      -OutFile $PtauFile
}

Write-Host "3) Trusted setup (Groth16)..."
snarkjs groth16 setup "circuits\circom\wisard.r1cs" `
    $PtauFile $Zkey0 -q
snarkjs zkey contribute $Zkey0 $ZkeyFinal -q `
    -n "initial contribution"

Write-Host "4) Gerando witness (WASM → WTN)..."
node circuits\circom\wisard_js\generate_witness.js `
    "circuits\circom\wisard.wasm" $WitnessJson $WitnessWtn

Write-Host "5) Gerando prova..."
snarkjs groth16 prove $ZkeyFinal $WitnessWtn `
    $ProofJson $PublicJson -q

Write-Host "6) Verificando prova..."
snarkjs groth16 verify $VerificationKey `
    $PublicJson $ProofJson

Write-Host "`n✅ Pipeline concluída! Proof verificada."
