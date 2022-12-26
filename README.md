<h1 align="center">
  <br>
  Comparison of Algorithms for Solving Traveling Salesman Problem</a>
  <br>
  <h5 align="center"></h5>
  <br>
</h1>

<h1 align="center">
 <img src="https://img.shields.io/badge/Python-3.9-red" alt="python badge">
 <img src="https://img.shields.io/badge/optimization-problem-blue" alt="docker badge">
 <img src="https://img.shields.io/badge/version-1.1.8-orange" alt="version badge">
 <img src="https://img.shields.io/badge/vitrual-3.9-green" alt="venv">
</h1>


# Travelling salesman problem

The travelling salesman problem (also called the travelling salesperson problem or TSP) asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?" It is an NP-hard problem in combinatorial optimization, important in theoretical computer science and operations research.


# 1. Getting Started

This repository is an implementation for the paper `Comparison of Algorithms for Solving Traveling Salesman Problem`, we have implemented the three proposed algorithms in the paper for different numbers of capital cities around the world.

# 2. Prerequisites

Please make sure that your system has the following platforms:


- `python3.9`

# 3. Installation

1. First get the code by either run this command through SSH:

   ```bash
   git clone git@github.com:karmelyoei/TSP.git
   ```

   or through HTTPS:

   ```bash
   git clone https://github.com/karmelyoei/TSP.git
   ```

3. Install environment:

   ```bash
   virtualenv -p python3.9 .venv && source .venv/bin/activate
   # or, if you don't have 'virtualenv' util installed:
   # python -m venv .venv && source .venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```


# 4. Development

These steps will assist you in running the code .


1. Start the each algorithm file using the following command:
   ```bash
   python3 -m mprof run ./SA_run.py

   ```
All the results will be saved inside the `./results/` folder so make sure you have created this folder in the root of this repo.

# 5. Troubleshooting

If you have encountered any problems while running the code, please open a new issue in this repo and label it bug, and we will assist you in resolving it.

# 6. Code Owners

@karmelyoei :sunglasses:

# 7. License

Our reposiorty is licensed under the terms of the MIT see the license [here!](https://github.com/karmelyoei/TSP/blob/main/LICENSE)


# 8. Contact

If you'd like to contact me send me an email karmel.salah@gmail.com
