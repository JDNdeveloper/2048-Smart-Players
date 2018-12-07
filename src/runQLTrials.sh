#/bin/bash

SIZE=$1
ID=$2
BSIZE=${SIZE}x${SIZE}
SEQUENCES=sequences/${BSIZE}_sequences.yaml
(set -x; time python -u Main.py --player ql --sequences \
    ${SEQUENCES} --size ${SIZE}) 2>&1 \
    | tee data/${BSIZE}_QL_data_${ID}.txt
