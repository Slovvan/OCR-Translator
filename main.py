import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from ocr import OcrWindow
from pruebas import MainWindow

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Translator")
        self.setGeometry(500, 600, 300, 400)
        
        self.initUI()

       
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"
    
        bWindowOcr = QPushButton("Start Ocr", self)
        bWindowOcr.setStyleSheet(button_style)
        bWindowOcr.clicked.connect(self.ocrwindow_onClick)

        bWindowlog = QPushButton("View Log text", self)
        bWindowlog.setStyleSheet(button_style)
        bWindowlog.clicked.connect(self.logWindow_onClick)

        grid = QGridLayout()
        grid.addWidget(bWindowOcr, 0, 1)
        grid.addWidget(bWindowlog, 0, 2)

        central_widget.setLayout(grid)

    def ocrwindow_onClick(self):
        self.newWindow = OcrWindow()  # Crear ventana directamente con su clase
        self.newWindow.show()
    
    def logWindow_onClick(self):
        self.newWindow = MainWindow()  # Crear ventana directamente con su clase
        self.newWindow.show()
                

    

def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

