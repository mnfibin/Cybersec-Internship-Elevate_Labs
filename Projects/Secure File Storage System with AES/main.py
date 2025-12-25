import os
import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import Main

os.makedirs("data/encrypted", exist_ok=True)
os.makedirs("data/decrypted", exist_ok=True)

app = QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())
