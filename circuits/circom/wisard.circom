pragma circom 2.0.0;

/*
Minimal Bloom-WiSARD verifier:
- inBits  : vetor privado de bits (M = 1024)
- expected: classe pública (0-39)
  Divide inBits em N blocos de tamanho fixo, soma por bloco, faz argmax e
  garante que argmax == expected.
*/

template WiSARD(M, N) {
    signal input inBits[M];
    signal input expected;     // public
    signal output out;

    var block = M / N;
    signal sums[N];
    for (var i = 0; i < N; i++) {
        sums[i] <== 0;
        for (var j = 0; j < block; j++) {
            sums[i] <== sums[i] + inBits[i*block + j];
        }
    }

    // argmax
    var maxIdx = 0;
    var maxVal = sums[0];
    for (var k = 1; k < N; k++) {
        var isGreater = sums[k] > maxVal;
        maxVal = isGreater * sums[k] + (1 - isGreater) * maxVal;
        maxIdx = isGreater * k       + (1 - isGreater) * maxIdx;
    }

    out <== maxIdx;
    out === expected;
}

component main {public [expected]} = WiSARD(1024, 40);
