from PySide6.QtWidgets import QLabel, QMainWindow, QStackedWidget

from image_nest.presentation.image_screening_page import ImageScreeningPage

class MainWindow(QMainWindow):
  def __init__(self) -> None:
    super().__init__()

    self.setWindowTitle("Image Nest")
    self.resize(1200, 720)

    self.stack = QStackedWidget()
    self.setCentralWidget(self.stack)

    self.screening = ImageScreeningPage()
    self.stack.addWidget(self.screening)

    self.show_screening()

  def show_screening(self):
    self.stack.setCurrentWidget(self.screening)
