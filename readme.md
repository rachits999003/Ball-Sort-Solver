# 🧪 Ball Sort Puzzle Solver (DFS-based)

This is a GUI-based **Ball Sort Puzzle Solver** built with `tkinter` in Python.  
It includes both **manual gameplay** and an automatic **Depth-First Search (DFS)** solver with backtracking.

---

## 🎮 Features

- Visual interface to play or watch the puzzle being solved
- Custom puzzle creation and color editing
- DFS-based puzzle solver with backtracking
- Animation of each solving step
- Support for random puzzle generation

---

## 🧠 How It Solves the Puzzle

The solver uses **Depth-First Search (DFS)** with backtracking to explore all valid moves recursively.  
It tries to move colored balls between tubes, tracking visited states to avoid loops. Once the goal state is reached (all tubes sorted by color), it backtracks to reconstruct the solution path.

> ⚠ DFS does **not guarantee the shortest solution**, but it finds a working one.

---

## 🛠️ Requirements

- Python 3.7+
- No external libraries needed (uses `tkinter`, built-in in Python)
