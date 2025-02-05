import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QRadioButton, QLabel, QButtonGroup
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

        #Lang selection
        self.org = ""
        self.dest = ""

       
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

        frm = QLabel("From:")
        to = QLabel("To: ")

        es1 = QRadioButton("Español")
        es2 = QRadioButton("Español")
        en1 = QRadioButton("English")
        en2 = QRadioButton("English")
        ja1 = QRadioButton("日本語")
        ja2 = QRadioButton("日本語")
        fr1 = QRadioButton("Français")
        fr2 = QRadioButton("Français")
        
        fromGroup = QButtonGroup(self)
        fromGroup.buttonClicked.connect(lambda button: self.Selectlanguage(button.text(), "origin"))
        fromGroup.addButton(es1)
        fromGroup.addButton(en1)
        fromGroup.addButton(ja1)
        fromGroup.addButton(fr1)
        
        toGroup = QButtonGroup(self)
        toGroup.buttonClicked.connect(lambda button: self.Selectlanguage(button.text(), "destination")) #get clicked radiobutton and send name
        toGroup.addButton(es2)
        toGroup.addButton(en2)
        toGroup.addButton(ja2)
        toGroup.addButton(fr2)

        grid = QGridLayout()
        grid.addWidget(frm, 0,1)
        grid.addWidget(to, 0,2)
        grid.addWidget(es1, 1,1)
        grid.addWidget(es2, 1,2)
        grid.addWidget(en1, 2,1)
        grid.addWidget(en2, 2,2)
        grid.addWidget(ja1, 3,1)
        grid.addWidget(ja2, 3,2)
        grid.addWidget(fr1, 4,1)
        grid.addWidget(fr2, 4,2)
        grid.addWidget(self.bWindowOcr, 5, 1)
        grid.addWidget(self.bWindowLog, 5, 2)

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

    def Selectlanguage(self, lang, group):
        if(lang == "Español"):
            if group == "origin":
                self.org = "es"
            else:
                self.dest = "es"
        elif(lang == "English"):
            if group == "origin":
                self.org = "en"
            else:
                self.dest = "en"
        elif(lang == "日本語"):
            if group == "origin":
                self.org = "ja"
            else:
                self.dest = "ja"
        elif(lang == "Français"):
            if group == "origin":
                self.org = "fr"
            else:
                self.dest = "fr"
        print(self.org, self.dest)
        self.ocr_instance.selectLang(self.org)
        
        self.ocr_instance.log_window.selectLang(self.org)
        self.ocr_instance.log_window.desLang = self.dest
            

       

def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

