"""Entry point for running the Kiwoom stock collector."""

from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from kiwoom.kiwoom import Kiwoom


class Main:
    def __init__(self) -> None:
        print("Search Program")
        self.app = QApplication(sys.argv)
        self.kiwoom = Kiwoom()


if __name__ == "__main__":
    Main()
