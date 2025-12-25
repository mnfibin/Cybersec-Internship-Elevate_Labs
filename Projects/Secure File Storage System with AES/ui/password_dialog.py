import random, string
from PyQt5 import QtCore, QtWidgets, QtGui


def crack_seconds(p):
    pool = 0
    if any(c.islower() for c in p): pool += 26
    if any(c.isupper() for c in p): pool += 26
    if any(c.isdigit() for c in p): pool += 10
    if any(c in "!@#$%^&*()-_=+[{]}:;" for c in p): pool += 32
    if pool == 0: return 0
    return (pool ** len(p)) / 2e10


class SecureKeyboard(QtWidgets.QWidget):
    def __init__(self, parent, input):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.input = input
        self.setStyleSheet("""
            QWidget{background:#141414;border-radius:14px;}
            QPushButton{background:#242424;color:white;border-radius:8px;padding:6px;}
            QPushButton:hover{background:#00ffaa;color:black;}
        """)
        grid = QtWidgets.QGridLayout(self)
        keys = list(string.ascii_letters + string.digits + "!@#$%&*")
        random.shuffle(keys)
        for i,k in enumerate(keys):
            b = QtWidgets.QPushButton(k)
            b.clicked.connect(lambda _,x=k:self.input.insert(x))
            grid.addWidget(b, i//10, i%10)


class PasswordDialog(QtWidgets.QDialog):
    def __init__(self, encryption_mode=True):
        super().__init__()
        self.resize(480, 300 if encryption_mode else 220)
        self.setModal(True)
        self.setWindowTitle("Enter Password")

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(10)

        self.input = QtWidgets.QLineEdit()
        self.input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input.setStyleSheet("""
            QLineEdit{background:#111;border:2px solid #00ffaa;
            color:white;border-radius:12px;padding:12px;font-size:16px;}
        """)
        lay.addWidget(self.input)

        # show password
        self.show = QtWidgets.QCheckBox("Show password")
        self.show.setStyleSheet("color:#bbb;")
        self.show.toggled.connect(lambda v:
            self.input.setEchoMode(QtWidgets.QLineEdit.Normal if v else QtWidgets.QLineEdit.Password))
        lay.addWidget(self.show)

        # strength section only for encryption
        if encryption_mode:
            self.state = QtWidgets.QLabel("No Password")
            self.state.setAlignment(QtCore.Qt.AlignCenter)
            self.state.setStyleSheet("font-size:18px;color:#aaa;")
            lay.addWidget(self.state)

            self.bar = QtWidgets.QProgressBar()
            self.bar.setTextVisible(False)
            self.bar.setFixedHeight(18)
            self.bar.setStyleSheet("QProgressBar{background:#222;border-radius:9px;} QProgressBar::chunk{border-radius:9px;}")
            lay.addWidget(self.bar)

            self.time_lbl = QtWidgets.QLabel("Time to crack: 0 seconds")
            self.time_lbl.setAlignment(QtCore.Qt.AlignCenter)
            self.time_lbl.setStyleSheet("color:#888;")
            lay.addWidget(self.time_lbl)

            self.input.textChanged.connect(self.update_strength)

        # keyboard
        self.kbtn = QtWidgets.QPushButton("Show Secure Keyboard")
        self.kbtn.setStyleSheet("border-radius:12px;padding:10px;")
        lay.addWidget(self.kbtn)

        self.keyboard = None
        self.kbtn.clicked.connect(self.toggle_keyboard)

        ok = QtWidgets.QPushButton("OK")
        ok.setStyleSheet("background:#00ffaa;color:black;border-radius:14px;padding:12px;")
        ok.clicked.connect(self.accept)
        lay.addWidget(ok)

        self.input.returnPressed.connect(self.accept)

    def toggle_keyboard(self):
        if self.keyboard and self.keyboard.isVisible():
            self.keyboard.close()
            self.keyboard = None
        else:
            self.keyboard = SecureKeyboard(self, self.input)
            self.keyboard.move(self.mapToGlobal(QtCore.QPoint(20, self.height())))
            self.keyboard.show()

    def update_strength(self):
        t = crack_seconds(self.input.text())
        if t == 0:
            self.state.setText("No Password")
            self.bar.setStyleSheet("QProgressBar::chunk{background:#666}")
        elif t < 60:
            self.state.setText("Weak")
            self.bar.setStyleSheet("QProgressBar::chunk{background:red}")
        elif t < 3600:
            self.state.setText("Medium")
            self.bar.setStyleSheet("QProgressBar::chunk{background:orange}")
        else:
            self.state.setText("Very Strong")
            self.bar.setStyleSheet("QProgressBar::chunk{background:#00ff88}")

        if t < 60: unit="seconds"
        elif t < 3600: unit="minutes"; t//=60
        elif t < 86400: unit="hours"; t//=3600
        elif t < 31536000: unit="days"; t//=86400
        else: unit="years"; t//=31536000
        self.time_lbl.setText(f"Time to crack: {int(t)} {unit}")

    def get(self):
        self.exec_()
        return self.input.text()
