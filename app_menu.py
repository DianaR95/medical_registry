
# Aplicatia contine un registru medical, cu medici de familie si apartinatori
# medicul de familie sa se logheze cu CNP ul
# sa existe un admin care adauga sau sterge un medic, dar si sa vada toti medicii personali
# aplicatia sa contina optiunea ca medicul sa adauge un pacient nou daca CNP ul nu exista in registru
# medicul sa mute un pacient din regsitrul altui medifc de familie cu recunosterea CNP ului
# medicul sa creeze bilet de trimitere personalizat in functie de specialitate si clinica

from PyQt6 import QtWidgets


import sys
from PyQt6 import QtWidgets
from login import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())