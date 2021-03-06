[REPORT](https://github.com/AishwaryaBalyaya10/Info6205-PSA-FinalProject-TicTacToe/blob/main/docs/The%20Menace.pdf)

# Introduction

The aim of this project to implement the [MENACE: Machine Educable Noughts And Crosses Engine](https://people.csail.mit.edu/brooks/idocs/matchbox.pdf). Donald Michie, an artificial intelligence researcher, devised and built a mechanical computer out of 304 matchboxes in 1961 to train it in game of tic-tac-toe by playing againts human opponents. Given a source,destination and a mask image, our goal is to generate a realistic composite belnded image. We have used TensorFlow to implement this paper.

# Team Members
- Aishwarya Balyaya NUID - 001586556
- Niul Panvalkar NUID - 002950308
- Shubhang Shah NUID - 002111376
# Requirements

- python3.8
- poetry
- make

# Table Of Contents

- [Installations](#installation)
- [Quick Start](#quick-starts)
- [Folder Structure](#folder-structure)
- [Inspirations](#implementation-flow)

# Installations

Please make sure you have installed python3.8, poetry and make for this project.

- [python3.8](https://www.python.org/downloads/release/python-380/)
- [poetry](https://python-poetry.org/docs/)
- make

# Quick Start

We use `Poetry` on Python 3.8 and each method can be run using

- Download required libraries for the project

```bash
make requirements
```

- Train menace with random human moves

```bash
make menace
```

- Play with menace

```bash
make minmax
```

- Run test cases

```bash
make test
```
## Folder Structure

### Top-level directory layout

    .
    ├── logs                    # Log files
    ├── docs                    # Documentation files
    ├── ticTacToe               # Source files
    ├── tests                   # Automated tests
    ├── LICENSE
    └── README.md

### Source files

    .
    ├── ...
    ├── ticTacToe
    │   ├── utils               # Helper files
    │   ├── menace              # Random human moves with menace
    │   └── minmax              # Human play with menace
    └── ...

### Automated tests

    .
    ├── ...
    ├── test                     # Test files
    │   ├── test_combinations    # Unit test cases for combinations
    │   ├── test_plot            # Unit test cases for plot
    │   └── test_ternary         # Unit test cases for ternary
    └── ...

## References

- https://www.javatpoint.com/mini-max-algorithm-in-ai
- https://www.mscroggs.co.uk/blog/tags/menace
- http://www.se16.info/hgb/tictactoe.htm
- https://en.wikipedia.org/wiki/Burnside%27s_lemma
- https://levelup.gitconnected.com/minimax-algorithm-explanation-using-tic-tac-toe-game-22668694aa13
- https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_and_Crosses_Engine#Origin
- https://en.wikipedia.org/wiki/Burnside%27s_lemma