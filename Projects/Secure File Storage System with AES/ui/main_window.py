import os
from PyQt5 import QtWidgets, QtCore
from core.crypto_engine import encrypt_file, decrypt_file
from core.metadata import save_meta, load_meta
from core.lockout import check_lock, record_failure, reset_lock
from core.secure_delete import secure_delete
from ui.password_dialog import PasswordDialog

class VaultTile(QtWidgets.QFrame):
    activated=QtCore.pyqtSignal()
    dropped=QtCore.pyqtSignal(str)
    def __init__(self,t,s):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("tile")
        self.t=QtWidgets.QLabel(t)
        self.s=QtWidgets.QLabel(s)
        self.t.setAlignment(QtCore.Qt.AlignCenter)
        self.s.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        lay=QtWidgets.QVBoxLayout(self)
        lay.addStretch(); lay.addWidget(self.t); lay.addStretch(); lay.addWidget(self.s)
    def mousePressEvent(self,e): self.activated.emit()
    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls(): self.setProperty("hover",True); self.style().polish(self); e.accept()
    def dragLeaveEvent(self,e): self.setProperty("hover",False); self.style().polish(self)
    def dropEvent(self,e):
        self.setProperty("hover",False); self.style().polish(self)
        self.dropped.emit(e.mimeData().urls()[0].toLocalFile())

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1100,520)
        self.enc=VaultTile("ENCRYPT FILE","Drop file here to encrypt")
        self.dec=VaultTile("DECRYPT FILE","Drop encrypted file here")
        self.enc.activated.connect(lambda:self.pick(True))
        self.dec.activated.connect(lambda:self.pick(False))
        self.enc.dropped.connect(self.encrypt)
        self.dec.dropped.connect(self.decrypt)
        lay=QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.enc); lay.addWidget(self.dec)
        self.setStyleSheet("""
            QWidget{background:#0b0b0b;color:white;font-size:18px;}
            #tile{background:#161616;border-radius:50px;border:2px solid #333;}
            #tile:hover{border:2px solid #00ffaa;}
            QLabel{font-size:28px;}
        """)

    def pick(self,enc):
        f,_=QtWidgets.QFileDialog.getOpenFileName(self,"Select File")
        if f: self.encrypt(f) if enc else self.decrypt(f)

    def encrypt(self,path):
        pwd=PasswordDialog(True).get()
        if not pwd: return
        data,meta=encrypt_file(path,pwd)
        out="data/encrypted/"+os.path.basename(path)+".enc"
        open(out,"wb").write(data)
        save_meta(meta,out)
        wipe=QtWidgets.QMessageBox.question(self,"Secure Delete",
            "Do you want to securely delete the original file?",
            QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if wipe==QtWidgets.QMessageBox.Yes:
            secure_delete(path)
        QtWidgets.QMessageBox.information(self,"Done","Encrypted successfully")

    def decrypt(self,path):
        if not path.endswith(".enc"):
            QtWidgets.QMessageBox.warning(self,"Not Encrypted","Please encrypt this file first.")
            return
        try:
            load_meta(path)
        except:
            QtWidgets.QMessageBox.warning(self,"Not Encrypted","Encryption metadata missing.")
            return

        locked,remain=check_lock(path)
        if locked:
            QtWidgets.QMessageBox.warning(self,"File Locked",f"Try again after {remain} seconds.")
            return

        pwd=PasswordDialog(False).get()
        if not pwd: return
        try:
            plain=decrypt_file(path,pwd,load_meta(path))
            reset_lock(path)
        except:
            record_failure(path)
            QtWidgets.QMessageBox.critical(self,"Decryption Failed",
                "Password is incorrect.\nPlease type the correct password.")
            return

        out="data/decrypted/"+os.path.basename(path).replace(".enc","")
        open(out,"wb").write(plain)
        QtWidgets.QMessageBox.information(self,"Success","Decrypted successfully")
