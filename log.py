import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt


class logWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log")
        self.setGeometry(500, 600, 300, 400)
        
        self.initUI()
        
    
    def initUI(self):
        self.log_text = QTextEdit(self)
        self.log_text.setGeometry(0,0 , 300, 400)
        self.log_text.setReadOnly(True)


    def add_text(self, text):
        self.log_text.append(text)

def main():
    app = QApplication(sys.argv)
    window = logWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

