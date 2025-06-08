# Sliding Puzzle Game and Solver

This Python script implements a command-line version of a sliding puzzle game. The objective is to navigate a player through a grid, visiting every open cell. The core mechanic is that the player slides in a chosen direction until they hit an obstacle or the edge of the board.

The script includes an advanced solver that uses a **Breadth-First Search (BFS)** algorithm to find the optimal (shortest) sequence of moves to solve the puzzle from any given state.

---

## Features

- **Interactive Gameplay**: Play the game manually through the command line by entering directions (`w`, `a`, `s`, `d`).
- **Clear Board Representation**: The game board is displayed in the console with easy-to-understand symbols:
    - `☺`: Player's current position
    - `*`: Visited cell
    - `.`: Unvisited open cell
    - `■`: Wall/Obstacle
- **Optimal Puzzle Solver**: The `solve_puzzle()` method can find the solution with the minimum number of moves required to complete the game.
- **Solve from Any State**: The solver can be called at any point during a manual game to find the best way to finish from the current board state, acting as a "hint" or "auto-finish" system.

---

## How to Run

1.  **Save the Code**: Save the provided Python code into a file named `slider_puzzle.py`.
2.  **Open Terminal**: Open a terminal or command prompt.
3.  **Navigate to Directory**: Use the `cd` command to navigate to the folder where you saved `slider_puzzle.py`.
4.  **Execute Script**: Run the script with the following command:
    ```bash
    python slider_puzzle.py
    ```
5.  **Follow Prompts**: The game will start, and you can either play manually or watch the solver find the optimal solution as demonstrated in the `main()` function.

---

## Code Structure

The entire logic is encapsulated within the `SliderPuzzle` class.

### Key Methods

- **`__init__(self, board, player_r, player_c)`**
  - Initializes the game with a given board layout and player starting position.
  - Creates a pristine copy of the original board for the solver to reference.

- **`print_board(self)`**
  - Displays the current state of the game board, including the player's position and stats like moves made and remaining cells.

- **`move_player(self, direction)`**
  - Handles the logic for manual gameplay, sliding the player in the specified direction until an obstacle is met.

- **`solve_puzzle(self)`**
  - The core of the solver. It uses BFS to find the shortest sequence of moves to visit all remaining unvisited cells from the player's current position.

---

## Solving Algorithm: Breadth-First Search (BFS)

The solver finds the shortest path by modeling the puzzle as a state-space graph and exploring it with BFS.

1.  **State Definition**: A unique "state" in the puzzle is defined by a combination of:
    - The player's current position (which must be a "stopping point").
    - The set of all cells that have already been visited.

2.  **Pre-computation**: Before starting the search, the solver builds a `slide_graph`. This graph maps every possible stopping point on the board to a list of all other stopping points reachable from it in a single slide. This avoids recalculating slides repeatedly and makes the search much faster.

3.  **BFS Exploration**:
    - The search starts with the current state (player position and visited cells).
    - A queue is used to explore states layer by layer. It adds the initial state to the queue.
    - The algorithm repeatedly dequeues a state, finds all possible next states reachable in one move (using the pre-computed `slide_graph`), and enqueues them.
    - A `visited_states` set is maintained to ensure the algorithm doesn't process the same state twice, preventing infinite loops.

4.  **Finding the Solution**: Because BFS explores all 1-move paths before any 2-move paths, and so on, the **first time** it finds a state where all walkable cells have been visited, that path is guaranteed to be one of the solutions with the minimum possible number of moves.

