from PyQt6.QtCore import QSize, QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QGridLayout
)

class SolveWindow(QWidget):
    """

    """
    def __init__(self, maze, start, end):
        super().__init__()
        self.maze = maze
        self.start = start
        self.end = end
        self.moves_left = None

        page_layout = QHBoxLayout()
        self.maze_layout = QGridLayout()
        self.side_panel_layout = QVBoxLayout()
        self.controls_layout = QHBoxLayout()
        self.keypad_layout = QGridLayout()

        self.up_key = QPushButton("^")
        self.down_key = QPushButton("v")
        self.right_key = QPushButton("<")
        self.left_key = QPushButton(">")
        self.undo_btn = QPushButton("Undo")
        self.answer_btn = QPushButton("Give Up")

        self.ui_components()

        page_layout.addLayout(self.maze_layout)
        page_layout.addLayout(self.side_panel_layout)

        self.setLayout(page_layout)
        self.setFixedSize(QSize(800, 700))

    def ui_components(self):
        # keypad
        self.keypad_layout.addWidget(self.up_key, 0, 1)
        self.keypad_layout.addWidget(self.down_key, 2, 1)
        self.keypad_layout.addWidget(self.right_key, 1, 0)
        self.keypad_layout.addWidget(self.left_key, 1, 2)

        self.controls_layout.addLayout(self.keypad_layout)

        # undo button
        self.controls_layout.addWidget(self.undo_btn)

        self.side_panel_layout.addLayout(self.controls_layout)

        # moves label
        num_moves = QLabel("Number of moves left")
        self.side_panel_layout.addWidget(num_moves)
        self.side_panel_layout.addWidget(self.answer_btn)

        self.create_maze()

    def create_maze(self):
        maze = QLabel("Maze")
        self.maze_layout.addWidget(maze, 0, 1)

