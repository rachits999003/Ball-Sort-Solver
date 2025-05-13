# 🧪 Ball Sort Puzzle Solver (A-Star-based)

This is a GUI-based **Ball Sort Puzzle Solver** built with `tkinter` in Python.  
It includes an automatic **A-Star (A*)** solver with backtracking.

---

## 🎮 Features

- Visual interface to play or watch the puzzle being solved
- Custom puzzle creation and color editing
- A*-based puzzle solver with Hash-maps
- Animation of each solving step
- Support for random puzzle generation

---

## 🧠 How It Solves the Puzzle

The solver uses **A-Star (A*)** with Hash-maps to explore all valid moves recursively.  
It tries to move colored balls between tubes, tracking visited states to avoid loops. Once the goal state is reached (all tubes sorted by color), it returns the solution path.

---

## 🛠️ Requirements

- Python 3.7+
- No external libraries needed (uses `tkinter`, built-in in Python)
