#/bin/bash

SIZE=$1
ID=$2
SEQUENCES=sequences/exp-2-sequence.yaml
(set -x; time python -u Main.py --player ql --sequences \
    ${SEQUENCES} --size ${SIZE}) 2>&1 \
    | tee data/${SIZE}x${SIZE}_data_${ID}.txt
