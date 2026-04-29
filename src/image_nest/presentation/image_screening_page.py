from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QStackedLayout, QLabel, QFileDialog, QSizePolicy
from PySide6.QtGui import QPixmap, QResizeEvent, QShowEvent, QKeyEvent

from image_nest.application.image_screening.image_screening_session import ImageScreeningSession
from image_nest.application.settings.settings_repository import SettingsRepository

class ImageScreeningPage(QWidget):
  def __init__(self):
    super().__init__()

    layout = QStackedLayout(self)
    self.setLayout(layout)

    self.label = QLabel()
    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.label.setSizePolicy(
      QSizePolicy.Policy.Expanding,
      QSizePolicy.Policy.Expanding,
    )
    self.label.setStyleSheet("""
      QLabel {
        background-color: #222222;
      }
    """)
    layout.addWidget(self.label)

    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    self.session = ImageScreeningSession(self)
    self.session.image_changed.connect(self.showImage)

    self.pixmap: QPixmap | None = None

  def showEvent(self, event: QShowEvent) -> None:
    super().showEvent(event)

    if self.session.getFileCount() == 0:
      QTimer.singleShot(0, self.openInputDialog)
  
  def openInputDialog(self):
    app_settings = SettingsRepository.load()
    SettingsRepository.save(app_settings)

    input_dir = QFileDialog.getExistingDirectory(self)
    if input_dir is not None:
      self.session.start(Path(input_dir), app_settings=app_settings)

  def showImage(self, path: Path, index):
    self.pixmap = QPixmap(str(path))
    if self.pixmap.isNull():
      self.label.setText("画像を読み込めませんでした")
      self.pixmap = None
    self.updateScaledPixmap()

  def resizeEvent(self, event: QResizeEvent) -> None:
    super().resizeEvent(event)
    self.updateScaledPixmap()

  def updateScaledPixmap(self):
    if self.pixmap is None:
      return
    
    target_size = self.label.size()
    if target_size.width() <= 0 or target_size.height() <= 0:
      return

    scaledPixmap = self.pixmap.scaled(
      target_size,
      Qt.AspectRatioMode.KeepAspectRatio,
      Qt.TransformationMode.SmoothTransformation,                                
    )

    self.label.setPixmap(scaledPixmap)

  def keyPressEvent(self, event: QKeyEvent):
    if event.isAutoRepeat():
      return
    
    if event.key() == Qt.Key_Right:
      self.session.accept()
    elif event.key() == Qt.Key_Up:
      self.session.hold()
    elif event.key() == Qt.Key_Down:
      self.session.reject()
    elif event.key() == Qt.Key_Left:
      self.session.previous()
