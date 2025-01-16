import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from ocr import OcrWindow
from pruebas import MainWindow
from log import logWindow

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Translator")
        self.setGeometry(500, 600, 300, 400)
        
        self.initUI()

        self.windows = {}
        self.ocr_instance = OcrWindow()
        self.bWindowOcr
        self.bWindowLog

       
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"
    
        self.bWindowOcr = QPushButton("Start OCR", self)
        self.bWindowOcr.setStyleSheet(button_style)
        self.bWindowOcr.clicked.connect(self.ocrwindow_onClick)

        self.bWindowLog = QPushButton("Log of Text", self)
        self.bWindowLog.setStyleSheet(button_style)
        self.bWindowLog.clicked.connect(self.logWindow_onClick)

        grid = QGridLayout()
        grid.addWidget(self.bWindowOcr, 0, 1)
        grid.addWidget(self.bWindowLog, 0, 2)

        central_widget.setLayout(grid)

    def ocrwindow_onClick(self):
        window_name = "OCR" 
        if self.bWindowOcr.text() == "Start OCR":
            self.windows[window_name] = self.ocr_instance
            self.windows[window_name].show()
            self.bWindowOcr.setText("Close OCR")
        elif window_name in self.windows:  # Check if the OCR window is open
            self.windows[window_name].close()
            del self.windows[window_name]  # Remove from dictionary
            self.bWindowOcr.setText("Start OCR")
        print(self.windows)

    
    def logWindow_onClick(self):
        window_name = "logwindow"
        if window_name not in self.windows:
            self.windows[window_name] = self.ocr_instance.log_window
            self.windows[window_name].show()
        else:
            self.windows[window_name].raise_()
       

def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

