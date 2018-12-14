2048 Solver (CS 221 Fall 2018 Project)
========================

[![Build Status](https://travis-ci.com/jaynavar/CS221_Project_RMJ.svg?token=DesaacDGQoqJ7q1qhzeY&branch=master)](https://travis-ci.com/jaynavar/CS221_Project_RMJ)

**Authors:** Ruben Mayer (`rmayer99`), Magdy Saleh (`mksaleh`), Jayden Navarro (`jaynavar`)

# Repo Hierarchy

- `src` contains all of our source code.
- `submission` contains all of our submission PDFs.
- `src/data` contains all of our trials results.

# Running 2048

`Main.py` is the driver for our program, and includes a detailed `python2 Main.py --help` output.

For example, to run 10 iterations of Expectimax with depth 4 and probability cutoff 1e-4, you can use:

`python2 Main.py 10 --player EM --depth 4 --probCutoff 1e-4`.

To run 10 iterations of Q-Learning with training on you can use:

`python2 Main.py 10 --player QL --train`

To view the board as moves are executed, use the `--debug` flag.

# Replicating data collection

To collect data use the `runEMTrials.sh` and `runQLTrials.sh` scripts.

The parameters to these scripts are as follows:

`./runEMTrials.sh <board_size> <trial_number> <num_iters> <depth> <prob_cutoff>`

Example: `./runEMTrials.sh 4 7 100 6 1e-5`, runs a 4x4 for 100 iterations with depth 6 and probability cutoff 1e-5. The second parameter is a unique ID for the trial used for the output file. Results are outputted in `data/4x4_EM_data_7.txt`.

`./runQLTrials.sh <board_size> <trial_number>`

Example: `./runQLTrials.sh 4 7`, runs a 4x4 QL trial (utilizing the sequence file `4x4_sequences.yaml`) with unique trial ID 7. Results are outputted in `data/4x4_QL_data_7.txt`.
