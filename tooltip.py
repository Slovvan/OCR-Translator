import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint


class tooltipWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information window")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.info = QLabel("Informacion de prueba")
        self.info.setWordWrap(True)  # Allow text wrapping
        self.UI()


    def UI(self):
        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"
    
        widget_style = "background-color:#808080;"

        
        self.info.adjustSize()
        
        #Instance of horizontal part of the window
        HLayout = QHBoxLayout()
        HLayout.addStretch(1)
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
        """Update and display word details in the pop-up window."""
        text = f"<b>{info['word']}</b> -> {info['translation']}<br>"
        text += f"<b>Meaning: </b> {','.join(info['meanings'])}<br>"
        text += f"<b>Synonyms: </b> {','.join(info['synonyms']) if info['synonyms'] else 'none'}<br>"

        self.info.setText(text)
        self.adjustSize()
        self.move(info["position"]) # Move to cursor position
        self.show()


def main ():
    app = QApplication(sys.argv)
    window = tooltipWindow()
        # Example usage with test data
    example_data = {
        "word": "Bonjour",
        "translation": "Hello",
        "meanings": ["A greeting", "Good day"],
        "synonyms": ["Salut", "Coucou"],
        "position": QPoint(500, 300)  # Example position on screen
    }
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
