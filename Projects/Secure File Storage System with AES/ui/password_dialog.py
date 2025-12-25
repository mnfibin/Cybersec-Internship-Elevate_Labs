import random, string
from PyQt5 import QtCore, QtWidgets


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
            QWidget{background:#f4f4f4;border-radius:10px;}
            QPushButton{background:white;border-radius:6px;padding:6px;}
            QPushButton:hover{background:#00c896;color:white;}
        """)
        grid = QtWidgets.QGridLayout(self)
        keys = list(string.ascii_letters + string.digits + "!@#$%&*")
        random.shuffle(keys)
        for i,k in enumerate(keys):
            b = QtWidgets.QPushButton(k)
            b.clicked.connect(lambda _,x=k:self.input.insert(x))
            grid.addWidget(b,i//10,i%10)


class PasswordDialog(QtWidgets.QDialog):
    def __init__(self, encryption_mode=True):
        super().__init__()
        self.resize(520, 320 if encryption_mode else 230)
        self.setModal(True)
        self.setWindowTitle("Enter Password")

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(12)

        self.input = QtWidgets.QLineEdit()
        self.input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input.setPlaceholderText("Type a password")
        self.input.setStyleSheet(self._style("#bbb"))
        lay.addWidget(self.input)

        self.show = QtWidgets.QCheckBox("Show password")
        self.show.toggled.connect(lambda v:
            self.input.setEchoMode(QtWidgets.QLineEdit.Normal if v else QtWidgets.QLineEdit.Password))
        lay.addWidget(self.show)

        if encryption_mode:
            self.state = QtWidgets.QLabel("No Password")
            self.state.setAlignment(QtCore.Qt.AlignCenter)
            self.state.setStyleSheet("font-size:18px;")
            lay.addWidget(self.state)

            self.indicators = QtWidgets.QLabel("✖ Lowercase   ✖ Uppercase   ✖ Numbers   ✖ Symbols")
            self.indicators.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(self.indicators)

            self.charcount = QtWidgets.QLabel("0 characters")
            self.charcount.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(self.charcount)

            self.time_lbl = QtWidgets.QLabel("Time to crack: 0 seconds")
            self.time_lbl.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(self.time_lbl)

            self.input.textChanged.connect(self.update_strength)

        self.kbtn = QtWidgets.QPushButton("Show Secure Keyboard")
        lay.addWidget(self.kbtn)
        self.keyboard = None
        self.kbtn.clicked.connect(self.toggle_keyboard)

        ok = QtWidgets.QPushButton("OK")
        ok.setStyleSheet("background:#00c896;color:white;border-radius:10px;padding:12px;")
        ok.clicked.connect(self.accept)
        lay.addWidget(ok)
        self.input.returnPressed.connect(self.accept)

    def _style(self, color):
        return f"""
            QLineEdit {{
                border:2px solid {color};
                border-radius:10px;
                padding:10px;
                font-size:15px;
            }}
        """

    def toggle_keyboard(self):
        if self.keyboard and self.keyboard.isVisible():
            self.keyboard.close()
            self.keyboard = None
        else:
            self.keyboard = SecureKeyboard(self, self.input)
            self.keyboard.move(self.mapToGlobal(QtCore.QPoint(40, self.height())))
            self.keyboard.show()

    def update_strength(self):
        p = self.input.text()
        t = crack_seconds(p)

        low = any(c.islower() for c in p)
        up  = any(c.isupper() for c in p)
        num = any(c.isdigit() for c in p)
        sym = any(c in "!@#$%^&*()-_=+[{]}:;" for c in p)

        self.indicators.setText(
            f"{'✔' if low else '✖'} Lowercase   "
            f"{'✔' if up else '✖'} Uppercase   "
            f"{'✔' if num else '✖'} Numbers   "
            f"{'✔' if sym else '✖'} Symbols"
        )

        self.charcount.setText(f"{len(p)} characters")

        if t == 0:
            self.state.setText("No Password")
            self.input.setStyleSheet(self._style("#bbb"))
        elif t < 60:
            self.state.setText("Weak")
            self.input.setStyleSheet(self._style("red"))
        elif t < 3600:
            self.state.setText("Medium")
            self.input.setStyleSheet(self._style("orange"))
        elif t < 31536000:
            self.state.setText("Strong")
            self.input.setStyleSheet(self._style("#66cc00"))
        else:
            self.state.setText("Very Strong")
            self.input.setStyleSheet(self._style("#00c896"))

        if t < 60: unit="seconds"
        elif t < 3600: unit="minutes"; t//=60
        elif t < 86400: unit="hours"; t//=3600
        elif t < 31536000: unit="days"; t//=86400
        else: unit="years"; t//=31536000
        self.time_lbl.setText(f"Time to crack: {int(t)} {unit}")

    def get(self):
        self.exec_()
        return self.input.text()
