#/bin/bash

SIZE=$1
ID=$2
NUM_ITERS=$3
DEPTH=$4
PROB_CUTOFF=$5
BSIZE=${SIZE}x${SIZE}
SEQUENCES=sequences/${BSIZE}_sequences.yaml
(set -x; time python -u Main.py ${NUM_ITERS} --player em --depth ${DEPTH} \
    --probCutoff ${PROB_CUTOFF} --size ${SIZE}) 2>&1 \
    | tee data/${BSIZE}_EM_data_${ID}.txt
