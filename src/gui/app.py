"""Main application window."""

from __future__ import annotations

import threading

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTabWidget,
    QTextEdit, QFrame, QProgressBar, QMessageBox
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject

from ..crypto.keys import generate_keypair, RSAKeyPair
from .components.key_panel import KeyPanel
from .components.crypto_panel import CryptoPanel


# ── Background worker ────────────────────────────────────────────────────────

class _KeygenWorker(QObject):
    finished = pyqtSignal(object)   # RSAKeyPair
    error = pyqtSignal(str)

    def __init__(self, bits: int):
        super().__init__()
        self._bits = bits

    def run(self) -> None:
        try:
            kp = generate_keypair(self._bits)
            self.finished.emit(kp)
        except Exception as exc:
            self.error.emit(str(exc))


# ── Main window ──────────────────────────────────────────────────────────────

_DARK_BG   = "#1a1b26"
_PANEL_BG  = "#24283b"
_ACCENT    = "#7aa2f7"
_TEXT      = "#c0caf5"


class RSAApp(QMainWindow):
    _BIT_SIZES = ["512", "1024", "2048"]
    _DEFAULT_BITS = "1024"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA Encryption & Decryption")
        self.resize(860, 780)
        self.setMinimumSize(700, 600)
        self._thread: QThread | None = None
        self._apply_dark_theme()
        self._build()

    # ── Theme ────────────────────────────────────────────────────────

    def _apply_dark_theme(self) -> None:
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background: {_DARK_BG};
                color: {_TEXT};
            }}
            QTabWidget::pane {{
                border: 1px solid #414868;
                border-radius: 6px;
                background: {_PANEL_BG};
            }}
            QTabBar::tab {{
                background: #1a1b26;
                color: #565f89;
                padding: 8px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 12px;
            }}
            QTabBar::tab:selected {{
                background: {_PANEL_BG};
                color: {_ACCENT};
                font-weight: bold;
            }}
            QComboBox {{
                background: #292e42;
                color: {_TEXT};
                border: 1px solid #414868;
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 80px;
            }}
            QComboBox::drop-down {{ border: none; }}
            QScrollBar:vertical {{
                background: #1a1b26;
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: #414868;
                border-radius: 4px;
            }}
        """)

    # ── Layout ───────────────────────────────────────────────────────

    def _build(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_toolbar())

        self._progress = QProgressBar()
        self._progress.setRange(0, 0)   # indeterminate
        self._progress.setFixedHeight(3)
        self._progress.setTextVisible(False)
        self._progress.setStyleSheet(
            "QProgressBar { background:#1a1b26; border:none; }"
            f"QProgressBar::chunk {{ background:{_ACCENT}; }}"
        )
        self._progress.hide()
        root.addWidget(self._progress)

        root.addWidget(self._build_tabs())

    def _build_toolbar(self) -> QWidget:
        bar = QWidget()
        bar.setStyleSheet("background:#16161e; border-bottom:1px solid #414868;")
        bar.setFixedHeight(56)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("RSA Encryption Tool")
        title.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{_ACCENT}; background:transparent;")
        layout.addWidget(title)
        layout.addStretch()

        layout.addWidget(QLabel("Key size:"))

        self._bit_combo = QComboBox()
        self._bit_combo.addItems(self._BIT_SIZES)
        self._bit_combo.setCurrentText(self._DEFAULT_BITS)
        self._bit_combo.setFont(QFont("Arial", 11))
        layout.addWidget(self._bit_combo)

        layout.addSpacing(12)

        self._gen_btn = QPushButton("Generate Keys")
        self._gen_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self._gen_btn.setFixedHeight(36)
        self._gen_btn.setStyleSheet(
            "QPushButton {background:#E65100; color:white; border-radius:6px; padding:0 18px;}"
            "QPushButton:hover {background:#BF360C;}"
            "QPushButton:disabled {background:#555; color:#999;}"
        )
        self._gen_btn.clicked.connect(self._on_generate)
        layout.addWidget(self._gen_btn)

        return bar

    def _build_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.setFont(QFont("Arial", 12))

        self._crypto_panel = CryptoPanel()
        tabs.addTab(self._crypto_panel, "Encrypt / Decrypt")

        self._key_panel = KeyPanel()
        tabs.addTab(self._key_panel, "Key Details")

        tabs.addTab(self._build_about(), "About")
        return tabs

    def _build_about(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)

        box = QTextEdit()
        box.setReadOnly(True)
        box.setFont(QFont("Courier New", 11))
        box.setStyleSheet(
            f"background:{_PANEL_BG}; color:{_TEXT}; "
            "border:1px solid #414868; border-radius:6px; padding:12px;"
        )
        box.setPlainText(
            "RSA (Rivest–Shamir–Adleman) is a public-key cryptosystem.\n\n"
            "Key Generation\n"
            "  1. Pick two large distinct primes p and q.\n"
            "  2. Compute n = p·q  and  φ(n) = (p-1)·(q-1).\n"
            "  3. Choose e = 65537 (Fermat prime F4, universally standard).\n"
            "  4. Compute d = e⁻¹ mod φ(n) via the Extended Euclidean Algorithm.\n\n"
            "Encryption:   C = Mᵉ mod n   (uses public key  → share freely)\n"
            "Decryption:   M = Cᵈ mod n   (uses private key → keep secret)\n\n"
            "This tool uses:\n"
            "  • Miller-Rabin primality test (FIPS 186-5 witness counts)\n"
            "  • secrets module for cryptographically secure randomness\n"
            "  • Block encoding so arbitrary UTF-8 text can be encrypted\n"
            "  • Background thread for key generation (UI stays responsive)\n"
        )
        layout.addWidget(box)
        return w

    # ── Key generation ───────────────────────────────────────────────

    def _on_generate(self) -> None:
        bits = int(self._bit_combo.currentText())
        self._gen_btn.setEnabled(False)
        self._gen_btn.setText("Generating…")
        self._progress.show()

        self._thread = QThread()
        self._worker = _KeygenWorker(bits)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_keys_ready)
        self._worker.error.connect(self._on_generate_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.start()

    def _on_keys_ready(self, kp: RSAKeyPair) -> None:
        self._crypto_panel.set_keypair(kp)
        self._key_panel.update_keys(kp)
        self._progress.hide()
        self._gen_btn.setEnabled(True)
        self._gen_btn.setText("Generate Keys")

    def _on_generate_error(self, msg: str) -> None:
        self._progress.hide()
        self._gen_btn.setEnabled(True)
        self._gen_btn.setText("Generate Keys")
        QMessageBox.critical(self, "Key Generation Failed", msg)
