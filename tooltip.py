import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


class tooltipWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information window")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.info = QLabel("Informacion de prueba")
        self.UI()
        
    

    def UI(self):
        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"
    
        widget_style = "background-color:#808080;"

        
        self.info.setFixedSize(300, 100)
        
        # Instance of a button to save word in card
        button = QPushButton("save")
        button.setFixedSize(85, 30)
        button.setStyleSheet(button_style)

        #close window
        button.clicked.connect(self.saveInfo)

        
        #Instance of horizontal part of the window
        HLayout = QHBoxLayout()
        HLayout.addStretch(1)
        HLayout.addWidget(button)
        HLayout.addStretch(1)
        
        #Instance of vertical part of the window
        vLayout = QVBoxLayout()
        vLayout.addStretch(1)
        vLayout.addWidget(self.info)
        vLayout.addLayout(HLayout)

        #Create a box widget
        cLayout = QWidget(self)
        cLayout.setLayout(vLayout)
        cLayout.setStyleSheet(widget_style)
        cLayout.setMouseTracking(True)
        cLayout.installEventFilter(self)
        
       

        #set window with the new box window
        self.setCentralWidget(cLayout)
    
    def saveInfo(self, info):
        text = f"<b>{info["word"]}</b> -> {info["translation"]}<br>"
        text += f"<b>Meaning: </b> {','.join(info["meanings"])}<br>"
        text += f"<b>Synonyms: </b> {','.join(info["synonyms"]) if info["synonyms"] else 'none'}<br>"

        self.info.setText(text)
        self.move(info["position"])
        self.show()



def show_info(self, word, translation, synonyms, meanings, position):
        """Update and display word details in the pop-up window."""
        text = f"<b>{word}</b> → {translation}<br>"
        text += f"<b>Meaning (EN):</b> {', '.join(meanings)}<br>"
        text += f"<b>Synonyms (ES):</b> {', '.join(synonyms) if synonyms else 'None'}"

        self.label.setText(text)
        self.adjustSize()
        self.move(position)  # Move to cursor position
        self.show()



def main ():
    app = QApplication(sys.argv)
    window = tooltipWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
