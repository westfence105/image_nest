import os
from pathlib import Path
import shutil

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImageReader

from image_nest.application.settings.app_settings import AppSettings

class ImageScreeningSession(QObject):
  image_changed = Signal(Path, int)
  completed = Signal()
  error_occurred = Signal(str)

  def __init__(self, parent=None):
    super().__init__()
    self.image_files = []
    self.cur = 0

  def start(self, input_dir: Path, app_settings: AppSettings) -> None:
    self.app_settings = app_settings

    # rejectedフォルダの存在チェック/なければ作成
    rejected_path = input_dir / 'rejected'
    if not rejected_path.exists():
      rejected_path.mkdir()
    elif rejected_path.is_file():
      self.error_occurred.emit('入力フォルダにrejectedという名前のファイルがあります')
    
    self.input_dir = input_dir
    self.rejected_dir = rejected_path
    self.library_dir = app_settings.library_dir
    self.hold_dir = app_settings.hold_dir

    # ファイル一覧取得
    files = []
    for file in os.listdir(input_dir):
      files.append(input_dir / file)
    files.sort(key=os.path.getmtime, reverse=False)
    
    # 表示できる画像形式の拡張子のリスト
    formats = []
    for fmt in QImageReader.supportedImageFormats():
      formats.append(fmt.data().decode())

    # 画像ファイルを絞り込み
    for file in files:
      ext = file.suffix
      if len(ext) > 1 and formats.count(ext[1:]) > 0:
        self.image_files.append(Path(file))
    
    # 最初の画像を表示
    if self.image_files:
      self._seek(0)

  def _seek(self, offset):
    # 前後の画像に移動
    self.cur += offset
    if self.cur < len(self.image_files):
      self.image_changed.emit(self.image_files[self.cur], self.cur)
    else:
      self.completed.emit()

  def getFileCount(self):
    return len(self.image_files)
  
  def accept(self):
    # TODO: ライブラリへ移動&DB追加
    # 一旦仮で元のフォルダに戻す動作
    self._moveFile(self.input_dir)
    self._seek(1)
  
  def hold(self):
    # 保留フォルダへ移動
    self._moveFile(self.hold_dir)
    self._seek(1)
  
  def reject(self):
    # rejectフォルダへ移動
    self._moveFile(self.rejected_dir)
    self._seek(1)
  
  def previous(self):
    # 1つ前のファイルに戻る
    self._seek(-1)
  
  def _moveFile(self, dest_dir: Path) -> Path:
    file: Path = self.image_files[self.cur]
    
    dest = dest_dir / file.name
    if dest == file:
      # 同じフォルダ
      return
    
    if dest.exists():
      # ファイル名重複で連番付与
      num = 1
      while dest.exists():
        dest = dest_dir / '{0} ({1}){2}'.format(file.stem, num, file.suffix)
        num += 1

    # 移動を実行しパスを更新
    self.image_files[self.cur] = Path(shutil.move(file, dest_dir))
