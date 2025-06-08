import copy
import collections

class SliderPuzzle() :
    '''
    A class representing a sliding puzzle game.
    Board is a 2D array of integers where 0 represents an empty cell and 1 represents an obstacle.
    Player is represented by the character 'P'.
    '''
    
    def __init__(self, board: list[list[int]], player_r: int, player_c: int) -> None:
        
        self._original_board = copy.deepcopy(board)
        self._initial_player_r = player_r
        self._initial_player_c = player_c
        self._stop_points_mapping : dict[tuple[int, int], set[tuple[int, int]]] = {}
        self._stop_points : set[tuple[int, int]] = set()
        
        self.board = board
        if board[player_r][player_c] != 0 :
            print(f'Value of board at [{player_r}, {player_c}] is {board[player_r][player_c]}')
            print(f'Player position is {player_r}, {player_c}')
            raise Exception("Player cannot be on an obstacle!")
        self.count_unmarked_cells = sum(row.count(0) for row in self.board)
        
        self.player_r = player_r
        self.player_c = player_c
        self.moves = 0
        self.direction_mapping = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
        
        print("Game is solvable:", "Yes" if self.is_solvable() else "No")
        self.mark_as_visited(player_r, player_c)
        

    def print_board(self) -> None:
        """Prints the game board to the console with the player position marked."""
        board_with_player = copy.deepcopy(self.board)
        board_with_player[self.player_r][self.player_c] = 'P'
        for row in board_with_player:
            print(" ".join(str(cell) for cell in row))
        print(f"Moves: {self.moves}")
        print(f"Unmarked Cells: {self.count_unmarked_cells}")
        print("\n")
        
    def get_player_position(self) -> tuple[int, int] :
        """Returns the current position of the player."""
        return self.player_r, self.player_c
    
    def is_obstacle(self, r, c) -> bool :
        """Checks if a cell is an obstacle or end of the board."""
        return not (0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] != 1)
    
    def is_visited(self, r, c) -> bool:
        """Checks if a cell has been visited."""
        return self.board[r][c] == 'X'
    
    def mark_as_visited(self, r, c) -> None:
        """Mark a cell as visited."""
        if self.is_visited(r, c) or self.is_obstacle(r, c) :
            return 
        self.board[r][c] = 'X'
        self.count_unmarked_cells -= 1    
    
    def move_player(self, direction) -> None :
        """Moves the player in the specified direction until an obstacle or wall is hit."""
        
        if direction not in self.direction_mapping:
            print("Invalid direction! Use 'w', 'a', 's', or 'd'.")
            self.print_board()
            return 
        
        dr, dc = self.direction_mapping[direction]
        
        # Check if the move is valid
        if self.is_obstacle(self.player_r + dr, self.player_c + dc):
            print("Cannot move in that direction!")
            self.print_board()
            return
        
        self.moves += 1

        # Slide the player
        while True:
            next_r, next_c = self.player_r + dr, self.player_c + dc

            # Check for boundaries or obstacles
            if self.is_obstacle(next_r, next_c):
                break

            self.mark_as_visited(next_r, next_c)
            self.player_r, self.player_c = next_r, next_c

        self.print_board()
        
        return self.count_unmarked_cells == 0
        
    def get_stop_points(self, r, c) -> list[tuple[int, int]] :
        stop_points = []
        for dr, dc in self.direction_mapping.values() :
            next_r, next_c = r, c
            while not self.is_obstacle(next_r+dr, next_c+dc) :
                next_r+=dr
                next_c+=dc
            stop_points.append((next_r, next_c))
        return stop_points
    
    def is_solvable(self) -> bool :
        board = self.board
        player_r, player_c = self._initial_player_r, self._initial_player_c
        
        queue = collections.deque([(player_r, player_c)])
        visited_stops = {(player_r, player_c)}
        reachable_path_cells = {(player_r, player_c)}
        total_walkable_cells = sum(row.count(0) for row in board)
        while queue :
            curr_r, curr_c = queue.popleft()
            self._stop_points_mapping[(curr_r, curr_c)] = set()
            for dr, dc in self.direction_mapping.values() :
                next_r, next_c = curr_r, curr_c
                path = []
                while True :
                    r, c = next_r + dr, next_c + dc
                    if self.is_obstacle(r, c) :
                        break
                    next_r, next_c = r, c
                    path.append((r, c))
                
                new_stop = (next_r, next_c)
                if new_stop != (curr_r, curr_c) :
                    self._stop_points_mapping[(curr_r, curr_c)].add(new_stop)
                    if new_stop not in visited_stops :
                        visited_stops.add(new_stop)
                        queue.append(new_stop)
                        self._stop_points.add(new_stop)
                    
                for cell in path :
                    reachable_path_cells.add(cell)
                    
        if len(reachable_path_cells) != total_walkable_cells :
            print("Cells that cannot be covered are :")
            for r in range(len(board)) :
                for c in range(len(board[0])) :
                    if board[r][c] == 0 and (r, c) not in reachable_path_cells :
                        print(f"({r}, {c})")
            return False
        
        return True
    
    def get_list_unvisited_cells(self) :
        unvisited_cells = []
        for r in range(len(self.board)) :
            for c in range(len(self.board[0])) :
                if self.board[r][c] == 0 :
                    unvisited_cells.append((r, c))
        return unvisited_cells
    
    def get_stop_point_in_direction(self, r, c, direction) :
        dr, dc = self.direction_mapping[direction]
        next_r, next_c = r, c
        while not self.is_obstacle(next_r+dr, next_c+dc) :
            next_r+=dr
            next_c+=dc
        return next_r, next_c
    
    def solve_puzzle(self) -> list[str] | None:
        """
        Solves the puzzle from the CURRENT game state using Breadth-First Search (BFS)
        to find the shortest path to visit all remaining cells.
        """
        print("--- Finding Optimal Solution from Current State using BFS ---")
        
        # --- Step 1: Pre-compute a graph of all possible slides based on wall layout ---
        slide_graph = collections.defaultdict(list)
        all_non_wall_cells = {(r, c) for r, row in enumerate(self._original_board) for c, val in enumerate(row) if val == 0}

        for r_start, c_start in all_non_wall_cells:
            for direction, (dr, dc) in self.direction_mapping.items():
                if self.is_obstacle(r_start + dr, c_start + dc):
                    continue

                path_segment = []
                next_r, next_c = r_start, c_start
                while not self.is_obstacle(next_r + dr, next_c + dc):
                    next_r += dr
                    next_c += dc
                    path_segment.append((next_r, next_c))
                
                if path_segment:
                    end_point = path_segment[-1]
                    slide_graph[(r_start, c_start)].append((end_point, frozenset(path_segment), direction))

        # --- Step 2: BFS to find the shortest path that covers remaining cells ---
        all_walkable_cells = {(r, c) for r, row in enumerate(self._original_board) for c, val in enumerate(row) if val == 0}
        
        # Use the current player position as the starting point for the search.
        start_pos = (self.player_r, self.player_c)
        
        # The initial set of visited cells is what's currently marked 'X' on the board.
        initial_visited = frozenset(
            {(r, c) for r, row in enumerate(self.board) for c, val in enumerate(row) if val == 'X'} | {start_pos}
        )
        
        # State in queue: (current_position, frozenset_of_visited_cells, list_of_moves_from_current_state)
        bfs_queue = collections.deque([(start_pos, initial_visited, [])])
        visited_states = {(start_pos, initial_visited)}

        while bfs_queue:
            curr_pos, visited_cells, path = bfs_queue.popleft()

            # GOAL CONDITION: Have we visited every walkable cell?
            if visited_cells == all_walkable_cells:
                print("Optimal solution found!")
                return path

            # Explore neighbors (next possible slides) from the current stopping point.
            for next_pos, path_segment, direction in slide_graph.get(curr_pos, []):
                new_visited_cells = visited_cells.union(path_segment)
                
                if (next_pos, new_visited_cells) not in visited_states:
                    visited_states.add((next_pos, new_visited_cells))
                    new_path = path + [direction]
                    bfs_queue.append((next_pos, new_visited_cells, new_path))
        
        # If the queue becomes empty, no solution exists from the current state.
        print("Puzzle is NOT solvable from the current state.")
        return None      

def main():
    """Main function to run the game."""
    board = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    player_r, player_c = 3, 3
    game = SliderPuzzle(board, player_r, player_c)
    game.print_board()
    while True:
        direction = input("Enter a direction (w/a/s/d) | 'q' to quit | 'h' for help: ").lower()
        if direction=='h':
            print(game.solve_puzzle())
            continue
        if direction == 'q':
            print("Thanks for playing!")
            break
        solved = game.move_player(direction)
        if solved:
            print("You win!")
            print('Total Moves:', game.moves)
            break

if __name__ == "__main__":
    main()