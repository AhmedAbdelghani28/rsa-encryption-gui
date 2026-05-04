"""Encryption / Decryption panel."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ...crypto.rsa import encrypt_text, decrypt_text
from ...crypto.keys import RSAKeyPair


def _section_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Arial", 13, QFont.Weight.Bold))
    return lbl


def _small_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Arial", 11))
    return lbl


def _textbox(height: int = 80, mono: bool = True, readonly: bool = False) -> QTextEdit:
    box = QTextEdit()
    if mono:
        box.setFont(QFont("Courier New", 11))
    box.setFixedHeight(height)
    box.setReadOnly(readonly)
    box.setStyleSheet(
        "background:#1e1e2e; color:#cdd6f4; "
        "border:1px solid #444; border-radius:4px; padding:4px;"
    )
    return box


def _button(text: str, color: str, hover: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    btn.setFixedHeight(36)
    btn.setStyleSheet(
        f"QPushButton {{background:{color}; color:white; border-radius:6px; padding:0 16px;}}"
        f"QPushButton:hover {{background:{hover};}}"
        f"QPushButton:disabled {{background:#555; color:#999;}}"
    )
    return btn


def _separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet("color:#444;")
    return line


class CryptoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._keypair: RSAKeyPair | None = None
        self._build()

    def set_keypair(self, kp: RSAKeyPair) -> None:
        self._keypair = kp
        self._status.setText(f"Keys loaded  ({kp.bit_length}-bit)")
        self._status.setStyleSheet("color: #4CAF50; font-size: 11px;")

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        # ── Encrypt section ──────────────────────────────────────────
        layout.addWidget(_section_label("Encrypt"))
        layout.addWidget(_small_label("Plaintext message:"))

        self._plain_in = _textbox(height=90)
        self._plain_in.setPlaceholderText("Type your message here…")
        layout.addWidget(self._plain_in)

        enc_btn = _button("Encrypt  →", "#1565C0", "#0D47A1")
        enc_btn.clicked.connect(self._on_encrypt)
        layout.addWidget(enc_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(_small_label("Ciphertext (hex blocks):"))
        self._cipher_out = _textbox(height=90, readonly=True)
        layout.addWidget(self._cipher_out)

        layout.addWidget(_separator())

        # ── Decrypt section ──────────────────────────────────────────
        layout.addWidget(_section_label("Decrypt"))
        layout.addWidget(_small_label("Paste ciphertext (hex blocks):"))

        self._cipher_in = _textbox(height=90)
        layout.addWidget(self._cipher_in)

        dec_btn = _button("Decrypt  →", "#1B5E20", "#145218")
        dec_btn.clicked.connect(self._on_decrypt)
        layout.addWidget(dec_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(_small_label("Recovered plaintext:"))
        self._plain_out = _textbox(height=60, readonly=True)
        layout.addWidget(self._plain_out)

        # ── Status ───────────────────────────────────────────────────
        self._status = QLabel("No keys loaded — click Generate Keys first.")
        self._status.setFont(QFont("Arial", 11))
        self._status.setStyleSheet("color: gray;")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

    def _on_encrypt(self) -> None:
        if not self._keypair:
            QMessageBox.warning(self, "No Keys", "Please generate keys first.")
            return
        text = self._plain_in.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Please enter a message to encrypt.")
            return
        try:
            e, n = self._keypair.public_key
            blocks = encrypt_text(text, e, n)
            hex_blocks = " ".join(hex(b) for b in blocks)
            self._cipher_out.setPlainText(hex_blocks)
            self._cipher_in.setPlainText(hex_blocks)
        except Exception as exc:
            QMessageBox.critical(self, "Encryption Error", str(exc))

    def _on_decrypt(self) -> None:
        if not self._keypair:
            QMessageBox.warning(self, "No Keys", "Please generate keys first.")
            return
        raw = self._cipher_in.toPlainText().strip()
        if not raw:
            QMessageBox.warning(self, "Empty", "Please paste ciphertext to decrypt.")
            return
        try:
            blocks = [int(tok, 16) for tok in raw.split()]
            d, n = self._keypair.private_key
            plaintext = decrypt_text(blocks, d, n)
            self._plain_out.setPlainText(plaintext)
        except Exception as exc:
            QMessageBox.critical(self, "Decryption Error", str(exc))
