""""""

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
    """
    Main Window of Custom Maze Solver. Allows user to create a maze (presented as a grid) with preferred
    dimensions. Once 'Solve!' button is pressed, a new sub window will appear for user to solve the puzzle.
    """
    def __init__(self):
        """Initializes main window with grid dimensions, layout and widgets"""
        super().__init__()

        self.setWindowTitle("Solve Custom Maze")

        page_layout = QVBoxLayout()
        self.instructions_layout = QVBoxLayout()
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
        self.warning_label = QLabel("")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui_components()

        page_layout.addLayout(self.instructions_layout)
        page_layout.addLayout(self.input_layout)
        page_layout.addLayout(self.maze_layout)
        page_layout.addLayout(self.bottom_layout)
        page_layout.addWidget(self.warning_label)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setFixedSize(QSize(800, 850))
        self.setCentralWidget(widget)

    def ui_components(self):
        """Creates input boxes and initial grid as well as instructions and other label widgets"""
        # header info
        title = QLabel("Custom Maze Solver")
        title.setContentsMargins(60, 0, 60, 10)
        self.instructions_layout.addWidget(title)

        instructions = QLabel("Adjust the height and width of your maze below (max 20). \nClick on the cells "
                              "to create barriers for your maze and add the start and end \n"
                              "by clicking on either the start/end button and selecting your desired cell"
                              " immediately after. \nOnce you have completed your maze design, click 'Solve!' to "
                              "try and solve the puzzle or have the answer generated for you.")
        instructions.setContentsMargins(60, 0, 60, 10)
        self.instructions_layout.addWidget(instructions)

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

        self.input_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # maze layout
        self.create_grid()
        self.maze_layout.setRowStretch(20, 20)
        self.maze_layout.setColumnStretch(20, 20)
        self.maze_layout.setSpacing(0)

        self.maze_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # solve button
        solve_btn = QPushButton("Solve!")
        solve_btn.setFixedSize(90, 40)
        solve_btn.clicked.connect(self.solve_maze)
        self.bottom_layout.addWidget(solve_btn)

        self.bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def width_changed(self, val):
        """Sets new width and calls create_grid function to update grid
        Args:
            val: value of width obtained from spin box
        """
        old_width = self.width
        self.width = val

        if old_width > self.width:
            self.create_grid(True)
        self.create_grid()

    def height_changed(self, val):
        """Sets new height and calls create_grid function to update grid
        Args:
            val: value of height obtained from spin box
        """
        old_height = self.height
        self.height = val

        if old_height > self.height:
            self.create_grid(True)
        self.create_grid()

    def set_start(self, checked):
        """Setter for start toggle
        Args:
            checked: Boolean obtained when clicking start button
        """
        self.toggle_start = checked

    def set_end(self, checked):
        """Setter for end toggle
        Args:
            checked: Boolean obtained when clicking end button
        """
        self.toggle_end = checked

    def clear_flags(self):
        """Clears both start and end flags"""
        if self.start_flag:
            self.clear_start()

        if self.end_flag:
            self.clear_end()

    def clear_end(self):
        """Clears end flag"""
        end_cell = self.widget_grid[self.end_flag[0]][self.end_flag[1]]
        end_cell.setChecked(False)
        end_cell.setStyleSheet("background-color : white")

        self.end_flag = None

    def clear_start(self):
        """Clears start flag"""
        start_cell = self.widget_grid[self.start_flag[0]][self.start_flag[1]]
        start_cell.setChecked(False)
        start_cell.setStyleSheet("background-color : white")

        self.start_flag = None

    def create_grid(self, clear=False):
        """Creates a grid based on the height and width values. If old values are greater than
        new values, then the grid is cleared before creating grid
        Args:
            clear: defaulted to False, passed in True if grid was cleared
        """
        # if grid is cleared
        if clear:
            for i in reversed(range(self.maze_layout.count())):
                self.maze_layout.itemAt(i).widget().deleteLater()

            self.widget_grid = []

        # reinitialize widget and maze grid
        self.widget_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.maze_grid = [[False for x in range(self.width)] for y in range(self.height)]

        # create a button for each cell in the grid
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

    def reset_maze(self):
        """Resets size of grid"""
        self.height = 1
        self.width = 1
        self.create_grid(True)

    def toggle_cell(self, checked):
        """Toggles cell color and value (either maze barrier or not)
        Args:
            checked: boolean passed when clicking button
        """
        sending_cell = self.sender().objectName().split(",")
        width = int(sending_cell[0])
        height = int(sending_cell[1])

        if self.toggle_start is True:
            if (height, width) != self.end_flag:
                # unselect previous flag
                if self.start_flag:
                    previous_cell = self.widget_grid[self.start_flag[0]][self.start_flag[1]]
                    previous_cell.setChecked(False)
                    previous_cell.setStyleSheet("background-color : white")

                    self.maze_grid[self.start_flag[0]][self.start_flag[1]] = False

                # set start flag
                self.start_flag = (height, width)
                self.maze_grid[self.start_flag[0]][self.start_flag[1]] = False
                self.widget_grid[self.start_flag[0]][self.start_flag[1]].setStyleSheet("background-color : green")
                self.start_btn.setChecked(False)
                self.toggle_start = False
            else:
                self.warning_label.setText("**Cannot have start and end flag at same position. Unselect/move end flag"
                                           " or choose a different position**")

        elif self.toggle_end is True:
            if (height, width) != self.start_flag:
                # unselect previous flag
                if self.end_flag or self.maze_grid[height][width]:
                    previous_flag = self.widget_grid[self.end_flag[0]][self.end_flag[1]]
                    previous_flag.setChecked(False)
                    previous_flag.setStyleSheet("background-color : white")
                    self.maze_grid[self.end_flag[0]][self.end_flag[1]] = False

                self.end_flag = (height, width)
                self.maze_grid[self.end_flag[0]][self.end_flag[1]] = False
                self.widget_grid[self.end_flag[0]][self.end_flag[1]].setStyleSheet("background-color : red")
                self.end_btn.setChecked(False)
                self.toggle_end = False
            else:
                self.warning_label.setText("**Cannot have start and end flag at same position. Unselect/move start flag"
                                           " or choose a different position**")

        # player is placing regular maze barrier
        else:
            if (height, width) == self.start_flag:
                self.clear_start()
            elif (height, width) == self.end_flag:
                self.clear_end()
            else:
                self.widget_grid[height][width].setStyleSheet("background-color : black")
                self.maze_grid[height][width] = checked
                if checked is False:
                    self.widget_grid[height][width].setStyleSheet("background-color : white")

    def solve_maze(self):
        """Determines if maze meets conditions (must have start and finish). If met, a new sub window is opened
        to solve the maze"""
        if self.start_flag and self.end_flag:
            self.open_solve = SolveWindow(self.maze_grid, self.start_flag, self.end_flag)
            self.open_solve.show()
            self.warning_label.setText("")
        else:
            self.warning_label.setText("**Maze must have start and finish**")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()

