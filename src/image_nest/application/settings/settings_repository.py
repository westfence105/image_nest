from pathlib import Path
from PySide6.QtCore import QSettings
from image_nest.application.settings.app_settings import AppSettings

class SettingsRepository:
  def load() -> AppSettings:
    settings = QSettings("settings.ini", QSettings.Format.IniFormat)
    library_dir = Path(settings.value('libraryDir'))
    hold_dir = Path(settings.value('holdDir'))
    return AppSettings(library_dir=library_dir, hold_dir=hold_dir)
  
  def save(app_settings: AppSettings):
    settings = QSettings("settings.ini", QSettings.Format.IniFormat)
    settings.setValue('libraryDir', str(app_settings.library_dir))
    settings.setValue('holdDir', str(app_settings.hold_dir))

    