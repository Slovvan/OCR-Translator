import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt


class deckWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deck")
        self.setGeometry(700, 700, 300, 400)

        self.initUI()

    def initUI(self):
        pass

    def createCard(self, word, phrase):
        print (word, phrase)
        pass


def main():
    app = QApplication(sys.argv)
    window = deckWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()