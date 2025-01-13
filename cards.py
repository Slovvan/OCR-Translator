import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from ocr import OcrWindow
from pruebas import MainWindow

class cardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Translator")
        self.setGeometry(500, 600, 300, 400)
        
        self.initUI()

    def initUI(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = cardWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()