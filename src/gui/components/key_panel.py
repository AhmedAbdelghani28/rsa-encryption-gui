"""Key information panel — shows all RSA key components."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QTextEdit, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ...crypto.keys import RSAKeyPair


class KeyPanel(QWidget):
    _FIELDS = [
        "Bit length",
        "p",
        "q",
        "n  (modulus)",
        "φ(n)",
        "e  (public exponent)",
        "d  (private exponent)",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._boxes: dict[str, QTextEdit] = {}
        self._build()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)

        title = QLabel("RSA Key Components")
        title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(6)

        for row, name in enumerate(self._FIELDS):
            lbl = QLabel(name + ":")
            lbl.setFont(QFont("Arial", 11))
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            lbl.setMinimumWidth(160)

            box = QTextEdit()
            box.setFont(QFont("Courier New", 10))
            box.setReadOnly(True)
            box.setFixedHeight(44)
            box.setPlaceholderText("—")
            box.setStyleSheet("background:#1e1e2e; color:#cdd6f4; border:1px solid #444; border-radius:4px;")

            grid.addWidget(lbl, row, 0)
            grid.addWidget(box, row, 1)
            self._boxes[name] = box

        root.addLayout(grid)
        root.addStretch()

        self._note = QLabel("Generate keys using the toolbar button.")
        self._note.setFont(QFont("Arial", 10))
        self._note.setStyleSheet("color: gray;")
        self._note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._note)

    def update_keys(self, kp: RSAKeyPair) -> None:
        data = kp.summary()
        for name, box in self._boxes.items():
            box.setPlainText(data.get(name, "—"))
        self._note.setText("Keys generated successfully.")
        self._note.setStyleSheet("color: #4CAF50;")
