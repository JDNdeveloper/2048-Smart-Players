2048 Game Engine with Q-Learning and Expectimax AI agents (CS 221 Fall 2018 Project)
========================

[![Build Status](https://travis-ci.com/JDNdeveloper/2048-Smart-Players.svg?branch=master)](https://travis-ci.com/JDNdeveloper/2048-Smart-Players)

**Authors:** Ruben Mayer (`rmayer99`), Magdy Saleh (`mksaleh`), Jayden Navarro (`jaynavar`)

# Overview

This repo contains a 2048 game engine (Python), with a Q-Learning agent (Python) and an Expectimax agent (C++).

# Repo Hierarchy

- `src` contains all of our source code.
- `submission` contains all of our submission PDFs.
- `src/data` contains all of our trials results.

**NOTE:** Make sure to run `make` in `src/` before running `Main.py` with `--player EM` as it requires the `Expectimax` C++ library to run.

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

Example: `./runEMTrials.sh 4 7 100 6 1e-5` runs a 4x4 Expectimax trial for 100 iterations with depth 6 and probability cutoff 1e-5. The second parameter is a unique ID for the trial used for the output file. Results are outputted in `data/4x4_EM_data_7.txt`.

`./runQLTrials.sh <board_size> <trial_number>`

Example: `./runQLTrials.sh 4 7` runs a 4x4 QL trial (utilizing the sequence file `4x4_sequences.yaml`) with unique trial ID 7. Results are outputted in `data/4x4_QL_data_7.txt`.
