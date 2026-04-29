from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QDialog, QFormLayout, QLabel, QLineEdit

from image_nest.application.settings.app_settings import AppSettings
from image_nest.application.settings.settings_repository import SettingsRepository

class SettingsDialog(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent=parent)

    self.setWindowTitle("設定")
    self.setMinimumSize(300, 100)

    layout = QFormLayout(self)
    layout.setContentsMargins(20, 20, 20, 20)
    self.setLayout(layout)

    self.app_settings: AppSettings = SettingsRepository.load()

    self.input_library_dir = QLineEdit(self)
    self.input_library_dir.addAction(
      QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen),
      QLineEdit.ActionPosition.TrailingPosition,
    ).triggered.connect(self.selectLibraryDir)
    self.input_library_dir.setText(str(self.app_settings.library_dir))
    layout.addRow(QLabel("ライブラリ"), self.input_library_dir)

    self.input_hold_dir = QLineEdit(self)
    self.input_hold_dir.addAction(
      QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen),
      QLineEdit.ActionPosition.TrailingPosition,
    ).triggered.connect(self.selectHoldDir)
    self.input_hold_dir.setText(str(self.app_settings.hold_dir))
    layout.addRow(QLabel("保留フォルダ"), self.input_hold_dir)
    
  def selectLibraryDir(self):
    dir = QFileDialog.getExistingDirectory(self, dir=self.input_library_dir.text())
    if dir:
      self.input_library_dir.setText(str(dir))

  def selectHoldDir(self):
    dir = QFileDialog.getExistingDirectory(self, dir=self.input_hold_dir.text())
    if dir:
      self.input_hold_dir.setText(str(dir))
  
  def closeEvent(self, arg__1):
    super().closeEvent(arg__1)

    self.app_settings.library_dir = Path(self.input_library_dir.text())
    self.app_settings.hold_dir = Path(self.input_hold_dir.text())
    SettingsRepository.save(self.app_settings)

    self.accept()


