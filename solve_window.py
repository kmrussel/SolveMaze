from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout
)
from copy import deepcopy
from solve_puzzle import solve_puzzle


class SolveWindow(QWidget):
    """
    Sub Window for Custom Maze Solver. Allows user to either solve the maze using keypad keys or
    reveal the answer solved by solve_puzzle algorithm.
    """
    def __init__(self, maze, start, end):
        """Initializes maze requirements and the sub window's layout.
        Args:
            maze: 2D array of maze grid passed by main window, contains either True (barrier) or False (empty)
            start: tuple containing start coordinates (height, width)
            end: tuple containing end coordinates (height, width)
        """
        super().__init__()

        self.setWindowTitle("Solve Custom Maze")

        # maze structure and dimensions
        self.maze = deepcopy(maze)
        self.traverse_maze = deepcopy(maze)
        self.widget_grid = None

        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.start = start
        self.end = end

        # queue of moves made
        self.moves = [start]

        self.result = solve_puzzle(self.maze, self.start, self.end)
        if self.result:
            self.moves_left = len(self.result[0]) - 1
            self.num_moves = QLabel("Number of moves left: " + str(self.moves_left))
        else:
            self.moves_left = None
            self.num_moves = QLabel("Number of moves left: 0")

        # layout
        page_layout = QHBoxLayout()
        self.maze_layout = QGridLayout()
        self.side_panel_layout = QVBoxLayout()
        self.controls_layout = QHBoxLayout()
        self.keypad_layout = QGridLayout()

        self.ui_components()

        page_layout.addLayout(self.maze_layout)
        page_layout.addLayout(self.side_panel_layout)

        self.setLayout(page_layout)
        self.setFixedSize(QSize(900, 850))

    def ui_components(self):
        """Creates main components of sub window including:
            maze and side panel
            side panel -> control layout and button widgets (reset, give up, exit)
            control layout -> keypad buttons, undo button"""
        # instructions
        instructions = QLabel("Custom Maze Solver\n\n*Use the keypad below to traverse the maze \nstarting from the green "
                              "cell. You can use \nthe undo button to undo moves you made. \n*The 'Reset Maze' button will "
                              "reset all \nyour moves and bring you back to the start. \n*If you wish to only see the"
                              " answer or give up,\nselect the 'Give Up' Button. ")
        instructions.setContentsMargins(10, 10, 10, 10)
        instructions.setFixedWidth(300)
        self.side_panel_layout.addWidget(instructions)

        # keypad
        up_key = QPushButton("^")
        up_key.clicked.connect(self.move_up)
        up_key.setFixedSize(50, 50)
        self.keypad_layout.addWidget(up_key, 0, 1)

        down_key = QPushButton("v")
        down_key.clicked.connect(self.move_down)
        down_key.setFixedSize(50, 50)
        self.keypad_layout.addWidget(down_key, 2, 1)

        right_key = QPushButton(">")
        right_key.clicked.connect(self.move_right)
        right_key.setFixedSize(50, 50)
        self.keypad_layout.addWidget(right_key, 1, 2)

        left_key = QPushButton("<")
        left_key.clicked.connect(self.move_left)
        left_key.setFixedSize(50, 50)
        self.keypad_layout.addWidget(left_key, 1, 0)

        self.keypad_layout.setContentsMargins(0, 40, 0, 40)
        self.keypad_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.controls_layout.addLayout(self.keypad_layout)

        # undo button
        undo_btn = QPushButton("Undo")
        undo_btn.clicked.connect(self.undo_move)
        undo_btn.setFixedSize(60, 50)
        self.controls_layout.addWidget(undo_btn)

        self.side_panel_layout.addLayout(self.controls_layout)

        # remaining moves label
        self.num_moves.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.side_panel_layout.addWidget(self.num_moves)

        # bottom side panel buttons
        restart_btn = QPushButton("Reset Maze")
        restart_btn.clicked.connect(self.restart)
        restart_btn.setFixedSize(300, 40)
        self.side_panel_layout.addWidget(restart_btn)

        answer_btn = QPushButton("Give Up : Reveal the Answer")
        answer_btn.clicked.connect(self.give_up)
        answer_btn.setFixedSize(300, 40)
        self.side_panel_layout.addWidget(answer_btn)

        exit_btn = QPushButton("Exit / Create a New Maze")
        exit_btn.clicked.connect(lambda: self.close())
        exit_btn.setFixedSize(300, 40)
        self.side_panel_layout.addWidget(exit_btn)

        # create maze on left of layout
        self.create_maze()
        self.maze_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.maze_layout.setColumnStretch(20, 20)
        self.maze_layout.setRowStretch(20, 20)
        self.maze_layout.setSpacing(0)

    def move_up(self):
        """Allows player to move a up a cell if it is a valid move"""
        prev_move = self.moves[-1]
        new_move = (prev_move[0] - 1, prev_move[1])
        if self.check_move(new_move):
            self.move_cells(self.widget_grid[prev_move[0] - 1][prev_move[1]], new_move)

    def move_down(self):
        """Allows player to move down a cell if it is a valid move"""
        prev_move = self.moves[-1]
        new_move = (prev_move[0] + 1, prev_move[1])
        if self.check_move(new_move):
            self.move_cells(self.widget_grid[prev_move[0] + 1][prev_move[1]], new_move)

    def move_right(self):
        """Allows player to move right of a cell if its a valid move"""
        prev_move = self.moves[-1]
        new_move = (prev_move[0], prev_move[1] + 1)
        if self.check_move(new_move):
            self.move_cells(self.widget_grid[prev_move[0]][prev_move[1] + 1], new_move)

    def move_left(self):
        """Allows player to move left of a cell if its a valid move"""
        prev_move = self.moves[-1]
        new_move = (prev_move[0], prev_move[1] - 1)
        if self.check_move(new_move):
            self.move_cells(self.widget_grid[prev_move[0]][prev_move[1] - 1], new_move)

    def check_move(self, next_move):
        """Checks if next move is a valid move

        Args:
            next_move: tuple of the next move's coordinate

        Returns:
            returns True if move is value and false otherwise
        """
        # check if move is within the grid
        if 0 <= next_move[0] < self.height and 0 <= next_move[1] < self.width:
            # check if move is not a barrier and not a previous move
            if not self.traverse_maze[next_move[0]][next_move[1]] and next_move != self.start:
                return True
        return False

    def move_cells(self, next_cell, new_move):
        """If move is valid, new move's cell is updated. Checks if player has won, lost or still in progress

        Args:
            next_cell: button object of the next cell
            new_move: tuple of the next cells coordinate
        """
        next_cell.click()
        self.moves.append(new_move)
        self.moves_left -= 1

        # check for win or lose
        if self.moves[-1] == self.end and self.moves_left == 0:
            self.num_moves.setText("Number of moves left " + str(self.moves_left) + "\n You win!")
        elif self.moves_left == 0:
            self.num_moves.setText("Number of moves left " + str(self.moves_left) + "\n No more moves, try again.")
        else:
            self.num_moves.setText("Number of moves left " + str(self.moves_left))

    def undo_move(self):
        """Undoes previous move"""
        prev_move = self.moves.pop()
        prev_cell = self.widget_grid[prev_move[0]][prev_move[1]]
        prev_cell.click()
        self.moves_left += 1
        self.num_moves.setText("Number of moves left " + str(self.moves_left))

    def restart(self):
        """Undoes all moves"""
        for move in range(0, len(self.moves) - 1):
            self.undo_move()

    def create_maze(self):
        """Recreates maze that player has created in main window. Barriers can no longer be clickable."""
        self.widget_grid = [[0 for x in range(self.width)] for y in range(self.height)]

        # generates a button for each cell in maze
        for y in range(0, self.height):
            for x in range(0, self.width):
                cell = QPushButton()
                self.widget_grid[y][x] = cell
                cell.setFixedSize(30, 30)
                cell.setObjectName(str(x) + "," + str(y))

                if (y, x) == self.start:
                    cell.setStyleSheet("background-color: green")
                    cell.setCheckable(False)
                    cell.setChecked(True)

                elif (y, x) == self.end:
                    cell.setStyleSheet("background-color: red")
                    cell.setCheckable(True)
                    cell.clicked.connect(self.toggle_cell)

                # if cell is a barrier, do not make clickable
                elif self.maze[y][x]:
                    cell.setStyleSheet("background-color : black")
                    cell.setCheckable(False)
                    cell.setChecked(True)

                # traversable cell
                else:
                    cell.setStyleSheet("background-color: white; border: 1px solid black")
                    cell.setCheckable(True)
                    cell.clicked.connect(self.toggle_cell)

                self.maze_layout.addWidget(cell, y, x)

    def toggle_cell(self, checked):
        """Toggles cell if clicked

        Args:
            Checked: Boolean passed when clicking a button
        """
        sending_cell = self.sender().objectName().split(",")
        width = int(sending_cell[0])
        height = int(sending_cell[1])

        if (height, width) != self.end and checked:
            self.widget_grid[height][width].setStyleSheet("background-color : darkCyan")
        elif (height, width) != self.end and not checked:
            self.widget_grid[height][width].setStyleSheet("background-color: white")
        self.traverse_maze[height][width] = checked

    def give_up(self):
        """Shows answer to player by using the algorithm's result and moving through the cells according
        to the results"""
        # clear all previous moves
        self.restart()

        # use algorithm's result to move through the maze
        if self.moves_left:
            for move in self.result[1]:
                if move == "U":
                    self.move_up()
                elif move == "D":
                    self.move_down()
                elif move == "R":
                    self.move_right()
                elif move == "L":
                    self.move_left()
            self.num_moves.setText("Number of moves left:" + str(self.moves_left) + "\n Showing one of the shortest paths under "
                               + str(len(self.result[0]) - 1) + " moves")
        else:
            self.num_moves.setText("No Moves : There is no solution to this maze!")


