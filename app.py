from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
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

    """Creates a grid based on the height and width values. If old values are greater than 
    new values, then the grid is cleared before creating grid"""
    def create_grid(self, clear=False):
        if clear:
            for i in reversed(range(self.maze_layout.count())):
                self.maze_layout.itemAt(i).widget().deleteLater()

        for y in range(0, self.height):
            for x in range(0, self.width):
                cell = QPushButton("hi")
                cell.setFixedSize(self.cell_size, self.cell_size)
                cell.setCheckable(True)
                cell.clicked.connect(self.toggle_cell)
                self.maze_layout.addWidget(cell, y, x)

    """Resets size of grid"""
    def reset_maze(self):
        self.height = 1
        self.width = 1
        self.create_grid(True)

    """Toggles cell color and value (either maze barrier or not)"""
    def toggle_cell(self):
        pass
    
    """Solve Maze"""
    def solve_maze(self):
        pass


# class Color(QWidget):
#     def __init__(self, color):
#         super(Color, self).__init__()
#         self.setAutoFillBackground(True)
#
#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor(color))
#         self.setPalette(palette)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()

