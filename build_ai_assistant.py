# -*- coding: utf-8 -*-

import typing as T
import sys
import dataclasses
import subprocess
from pathlib import Path


@dataclasses.dataclass
class Paths:
    path_python_executable: Path = dataclasses.field()

    @property
    def dir_bin(self) -> Path:
        return self.path_python_executable.parent

    @property
    def path_bin_pip(self) -> Path:
        return self.dir_bin / "pip"

    def run_pip_install(self, package: str):
        args = [
            f"{self.path_bin_pip}",
            "install",
            package,
        ]
        subprocess.run(args, check=True)


paths = Paths(path_python_executable=Path(sys.executable).absolute())
