import os

from PyQt5 import QtCore, QtGui, QtWidgets

from core.crypto_engine import decrypt_file, encrypt_file
from core.lockout import check_lock, record_failure, reset_lock
from core.metadata import load_meta, save_meta
from core.secure_delete import secure_delete
from ui.password_dialog import PasswordDialog


class VaultTile(QtWidgets.QFrame):
    activated = QtCore.pyqtSignal()
    dropped = QtCore.pyqtSignal(str)

    def __init__(self, title, subtitle, icon):
        super().__init__()
        self.setAcceptDrops(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=28, xOffset=0, yOffset=8)
        )

        self.icon = QtWidgets.QLabel(icon)
        self.title = QtWidgets.QLabel(title)
        self.subtitle = QtWidgets.QLabel(subtitle)

        for lbl in (self.icon, self.title, self.subtitle):
            lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            lbl.setStyleSheet("background:transparent;")

        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.subtitle)

    def mousePressEvent(self, e):
        self.activated.emit()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            self.setStyleSheet(self.hover_style())
            e.accept()

    def dragLeaveEvent(self, e):
        self.setStyleSheet(self.normal_style())

    def dropEvent(self, e):
        self.setStyleSheet(self.normal_style())
        self.dropped.emit(e.mimeData().urls()[0].toLocalFile())

    def normal_style(self):
        return """
        QFrame{
            background:rgba(255,255,255,0.85);
            border:3px solid #00c896;
            border-radius:40px;
        }
        """

    def hover_style(self):
        return """
        QFrame{
            background:#00c896;
            border:3px solid #00c896;
            border-radius:40px;
            color:white;
        }
        """


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1150, 560)
        self.setWindowTitle("SecureVault")

        self.encrypt_tile = VaultTile("ENCRYPT FILE", "Click or drop file here", "🔒")
        self.decrypt_tile = VaultTile(
            "DECRYPT FILE", "Click or drop encrypted file here", "🔓"
        )

        self.encrypt_tile.setStyleSheet(self.encrypt_tile.normal_style())
        self.decrypt_tile.setStyleSheet(self.decrypt_tile.normal_style())

        self.encrypt_tile.activated.connect(lambda: self.pick(True))
        self.decrypt_tile.activated.connect(lambda: self.pick(False))
        self.encrypt_tile.dropped.connect(self.encrypt)
        self.decrypt_tile.dropped.connect(self.decrypt)

        brand = QtWidgets.QLabel("Developed by FIBIN MN")
        brand.setAlignment(QtCore.Qt.AlignCenter)
        brand.setStyleSheet("color:#888;font-size:11px;")

        tiles = QtWidgets.QHBoxLayout()
        tiles.addWidget(self.encrypt_tile)
        tiles.addWidget(self.decrypt_tile)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(tiles)
        layout.addWidget(brand)

        self.setStyleSheet("""
        QWidget{
            background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 #f4f7fb, stop:1 #eafef7);
            font-family:Segoe UI;
            color:#222;
        }
        QLabel{font-size:32px;font-weight:700;}
        """)

    def pick(self, enc):
        f, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File")
        if f:
            self.encrypt(f) if enc else self.decrypt(f)

    def encrypt(self, path):
        pwd = PasswordDialog(True).get()
        if not pwd:
            return
        data, meta = encrypt_file(path, pwd)
        out = "data/encrypted/" + os.path.basename(path) + ".enc"
        open(out, "wb").write(data)
        save_meta(meta, out)

        wipe = QtWidgets.QMessageBox.question(
            self,
            "Secure Delete",
            "Do you want to securely delete the original file?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if wipe == QtWidgets.QMessageBox.Yes:
            secure_delete(path)

        QtWidgets.QMessageBox.information(self, "Done", "Encrypted successfully")

    def decrypt(self, path):
        if not path.endswith(".enc"):
            QtWidgets.QMessageBox.warning(
                self, "Not Encrypted", "Please encrypt this file first."
            )
            return
        try:
            load_meta(path)
        except:
            QtWidgets.QMessageBox.warning(
                self, "Not Encrypted", "Encryption metadata missing."
            )
            return

        locked, remain = check_lock(path)
        if locked:
            QtWidgets.QMessageBox.warning(
                self, "File Locked", f"Try again after {remain} seconds."
            )
            return

        pwd = PasswordDialog(False).get()
        if not pwd:
            return
        try:
            plain = decrypt_file(path, pwd, load_meta(path))
            reset_lock(path)
        except:
            record_failure(path)
            QtWidgets.QMessageBox.critical(
                self,
                "Decryption Failed",
                "Password is incorrect.\nPlease type the correct password.",
            )
            return

        out = "data/decrypted/" + os.path.basename(path).replace(".enc", "")
        open(out, "wb").write(plain)
        QtWidgets.QMessageBox.information(self, "Success", "Decrypted successfully")
