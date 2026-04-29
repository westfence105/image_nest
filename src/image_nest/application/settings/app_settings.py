from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppSettings:
  library_dir: Path
  hold_dir: Path
