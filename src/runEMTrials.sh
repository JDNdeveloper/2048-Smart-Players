#/bin/bash

SIZE=$1
ID=$2
DEPTH=$3
PROB_CUTOFF=$4
BSIZE=${SIZE}x${SIZE}
SEQUENCES=sequences/${BSIZE}_sequences.yaml
(set -x; time python -u Main.py --player em --depth ${DEPTH} \
    --probCutoff ${PROB_CUTOFF} --size ${SIZE}) 2>&1 \
    | tee data/${BSIZE}_EM_data_${ID}.txt
