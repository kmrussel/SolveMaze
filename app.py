from PyQt6.QtCore import QSize, Qt
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
from solve_window import SolveWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Solve Custom Maze")

        page_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.maze_layout = QGridLayout()
        self.bottom_layout = QHBoxLayout()

        self.cell_size = 30
        self.height = 1
        self.width = 1
        self.maze_grid = [[False]]
        self.widget_grid = [[]]
        self.toggle_start = False
        self.toggle_end = False
        self.start_flag = None
        self.end_flag = None

        self.start_btn = QPushButton("Set Start")
        self.end_btn = QPushButton("Set End")
        self.ui_components()

        page_layout.addLayout(self.input_layout)
        page_layout.addLayout(self.maze_layout)
        page_layout.addLayout(self.bottom_layout)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setFixedSize(QSize(800, 700))
        self.setCentralWidget(widget)

    """Creates input boxes and initial grid"""
    def ui_components(self):
        # height components
        height_label = QLabel("Height")
        height_label.setFixedSize(50, 30)
        self.input_layout.addWidget(height_label)

        height_input = QSpinBox()
        height_input.setMinimum(1)
        height_input.setMaximum(20)
        height_input.setSingleStep(1)
        height_input.setFixedSize(100, 20)
        height_input.valueChanged.connect(self.height_changed)
        self.input_layout.addWidget(height_input)

        # width components
        width_label = QLabel("Width")
        width_label.setFixedSize(50, 20)
        self.input_layout.addWidget(width_label)

        width_input = QSpinBox()
        width_input.setMinimum(1)
        width_input.setMaximum(20)
        width_input.setSingleStep(1)
        width_input.setFixedSize(100, 20)
        width_input.valueChanged.connect(self.width_changed)
        self.input_layout.addWidget(width_input)

        # start flag
        self.start_btn.setFixedSize(80, 30)
        self.start_btn.setCheckable(True)
        self.start_btn.clicked.connect(self.set_start)
        self.start_btn.setChecked(self.toggle_start)
        self.input_layout.addWidget(self.start_btn)

        # end flag
        self.end_btn.setFixedSize(80, 30)
        self.end_btn.setCheckable(True)
        self.end_btn.clicked.connect(self.set_end)
        self.end_btn.setChecked(self.toggle_end)
        self.input_layout.addWidget(self.end_btn)

        # clear start and end
        clear_btn = QPushButton("Clear Flags")
        clear_btn.setFixedSize(80, 30)
        clear_btn.clicked.connect(self.clear_flags)
        self.input_layout.addWidget(clear_btn)

        # reset maze button
        reset_btn = QPushButton("Reset Maze")
        reset_btn.setFixedSize(80, 30)
        reset_btn.clicked.connect(self.reset_maze)
        self.input_layout.addWidget(reset_btn)

        self.input_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # maze component
        cell = QPushButton("hi")
        cell.setFixedSize(self.cell_size, self.cell_size)
        self.maze_layout.addWidget(cell, 0, 0)
        self.maze_layout.setColumnStretch(20, 20)
        self.maze_layout.setContentsMargins(0, 0, 0, 0)
        self.maze_layout.setSpacing(0)

        # alignment is off
        self.maze_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # solve button
        solve_btn = QPushButton("Solve!")
        solve_btn.setFixedSize(90, 40)
        solve_btn.clicked.connect(self.solve_maze)
        self.bottom_layout.addWidget(solve_btn)
        self.bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    """Sets new width and calls create_grid function to update grid"""
    def width_changed(self, val):
        old_width = self.width
        self.width = val

        if old_width > self.width:
            self.create_grid(True)
        self.create_grid()

    """Sets new height and calls create_grid function to update grid"""
    def height_changed(self, val):
        old_height = self.height
        self.height = val

        if old_height > self.height:
            self.create_grid(True)
        self.create_grid()

    def set_start(self, checked):
        self.toggle_start = checked

    def set_end(self, checked):
        self.toggle_end = checked

    def clear_flags(self):
        if self.start_flag:
            self.clear_start()

        if self.end_flag:
            self.clear_end()

    def clear_end(self):
        end_cell = self.widget_grid[self.end_flag[0]][self.end_flag[1]]
        end_cell.setChecked(False)
        end_cell.setStyleSheet("background-color : white")

        self.end_flag = None

    def clear_start(self):
        start_cell = self.widget_grid[self.start_flag[0]][self.start_flag[1]]
        start_cell.setChecked(False)
        start_cell.setStyleSheet("background-color : white")

        self.start_flag = None

    """Creates a grid based on the height and width values. If old values are greater than 
    new values, then the grid is cleared before creating grid"""
    def create_grid(self, clear=False):
        if clear:
            for i in reversed(range(self.maze_layout.count())):
                self.maze_layout.itemAt(i).widget().deleteLater()

            self.widget_grid = []

        self.widget_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.maze_grid = [[False for x in range(self.width)] for y in range(self.height)]

        for y in range(0, self.height):
            for x in range(0, self.width):
                cell = QPushButton()
                self.widget_grid[y][x] = cell
                cell.setStyleSheet("background-color: white")
                cell.setFixedSize(self.cell_size, self.cell_size)
                cell.setCheckable(True)
                cell.setObjectName(str(x) + "," + str(y))
                cell.clicked.connect(self.toggle_cell)
                cell.setChecked(self.maze_grid[y][x])
                self.maze_layout.addWidget(cell, y, x)

    """Resets size of grid"""
    def reset_maze(self):
        self.height = 1
        self.width = 1
        self.create_grid(True)

    """Toggles cell color and value (either maze barrier or not)"""
    def toggle_cell(self, checked):
        sending_cell = self.sender().objectName().split(",")
        width = int(sending_cell[0])
        height = int(sending_cell[1])

        if self.toggle_start is True:
            if (width, height) != self.end_flag:
                # unselect previous flag
                if self.start_flag:
                    previous_cell = self.widget_grid[self.start_flag[0]][self.start_flag[1]]
                    previous_cell.setChecked(False)
                    previous_cell.setStyleSheet("background-color : white")

                    self.maze_grid[self.start_flag[0]][self.start_flag[1]] = False

                # set start flag
                self.start_flag = (height, width)
                self.widget_grid[self.start_flag[0]][self.start_flag[1]].setStyleSheet("background-color : green")
                self.start_btn.setChecked(False)
                self.toggle_start = False

        elif self.toggle_end is True:
            if (width, height) != self.toggle_start:
                if self.end_flag:
                    previous_flag = self.widget_grid[self.end_flag[0]][self.end_flag[1]]
                    previous_flag.setChecked(False)
                    previous_flag.setStyleSheet("background-color : white")
                    self.maze_grid[self.end_flag[0]][self.end_flag[1]] = False

                self.end_flag = (height, width)
                self.widget_grid[self.end_flag[0]][self.end_flag[1]].setStyleSheet("background-color : red")
                self.end_btn.setChecked(False)
                self.toggle_end = False

        else:
            if (width, height) == self.start_flag:
                self.clear_start()
            elif (width, height) == self.end_flag:
                self.clear_end()
            else:
                self.widget_grid[height][width].setStyleSheet("background-color : black")
                self.maze_grid[height][width] = checked
                if checked is False:
                    self.widget_grid[height][width].setStyleSheet("background-color : white")

    """Solve Maze"""
    def solve_maze(self):
        if self.start_flag and self.end_flag:
            self.open_solve = SolveWindow(self.maze_grid, self.start_flag, self.end_flag)
            self.open_solve.show()
        else:
            # print label, must have start and finish
            pass


app = QApplication([])

window = MainWindow()
window.show()

app.exec()

