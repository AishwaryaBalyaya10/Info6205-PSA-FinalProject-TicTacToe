[REPORT]()

# Introduction

The aim of this project to implement the [MENACE: Machine Educable Noughts And Crosses Engine](https://people.csail.mit.edu/brooks/idocs/matchbox.pdf). Donald Michie, an artificial intelligence researcher, devised and built a mechanical computer out of 304 matchboxes in 1961 to train it in game of tic-tac-toe by playing againts human opponents. Given a source,destination and a mask image, our goal is to generate a realistic composite belnded image. We have used TensorFlow to implement this paper.

# Requirements

 - python3.8
 - poetry
 - make

# Table Of Contents

-  [Installations](#installation)
-  [Quick Start](#quick-starts)
-  [Implementation Flow](#implementation-flow)

# Installations
Please make sure you have installed python3.8, poetry and make for this project.
-   [python3.8](https://www.python.org/downloads/release/python-380/)
-   [poetry](https://python-poetry.org/docs/)
-   make

# Quick Start
Please make sure you have installed python3.8 and poetry for this project.

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