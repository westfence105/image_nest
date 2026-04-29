import sys

from PySide6.QtWidgets import QApplication

from image_nest.presentation.main_window import MainWindow
from image_nest.presentation.settings_dialog import SettingsDialog

def main() -> int:
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  return app.exec()

if __name__ == "__main__":
  raise SystemExit(main())
