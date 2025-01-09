#GUI grafical user interface
import sys
#modulo que da acceso a variables o func que interactuan con el interprete
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
#Qwidgets are the building blocks of a PYQT5 app && layout managers
#layout managers
from PyQt5.QtGui import QIcon, QFont, QPixmap #manipulation of images
from PyQt5.QtCore import Qt
#non-GUI classes important for pyQT5 apps

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #set interface
        
        self.setWindowTitle("OCR Translator")
        #x, y, width, height
        self.setGeometry(500, 300, 800, 600)
        self.setWindowIcon(QIcon("./img/icon.jpg"))
         #add the prefic self makes an var/object global
        self.button = QPushButton("Click", self)
        self.send = QPushButton("Send", self)
        self.label0 = QLabel("Push button", self)
        self.line_edit = QLineEdit(self)

        self.initUI()

     #customize interface
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

          #instanciation of label object
        label = QLabel("Hello", self)
        label1 = QLabel("Hello2", self)
        label.setFont(QFont("Arial", 50))
        label.setGeometry(0,0 , 10, 10)
        label.setStyleSheet("color: purple;"
                            "background-color: gray;"
                            "font-style: italic;"
                            "font-weight: bold;"
                            "text-decoration: underline;")
        
        self.send.setGeometry(0,0, 500, 400)
        self.send.clicked.connect(self.submit)
        self.line_edit.setGeometry(0,0, 500, 300)
        self.line_edit.setStyleSheet("font: arial;"
                                     "font-weight: bold;"
                                     "font-size: 40px;"
                                     )
        self.line_edit.setPlaceholderText("Enter your name")
        
        """     Alignment Vertically
        label.setAlignment(Qt.AlignTop)
        label.setAlignment(Qt.AlignBottom)
        label.setAlignment(Qt.AlignVCenter) """
        """     Aligment Horizontally 
        label.setAlignment(Qt.AlignRight)
        label.setAlignment(Qt.AlignLeft)
        label.setAlignment(Qt.AlignHCenter) """

        # Alignment vert. and hor.
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        #manage of layout

        """ sort verticallyh
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(label1) """

        """ sort horizontally
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(label1) """

        # Grid
        grid = QGridLayout()
        grid.addWidget(label, 0, 0)
        grid.addWidget(label1, 0,1)
        grid.addWidget(self.label0, 1,1)
        grid.addWidget(self.button, 1,0)
        grid.addWidget(self.line_edit, 2,0)
        grid.addWidget(self.send, 2,1)


        #set the new widget with everytjing inside
        central_widget.setLayout(grid)


       
        self.button.setGeometry(150,200,200,100)
        self.button.setStyleSheet("font-size: 40px")

        #signal.Connect(slot)
        self.button.clicked.connect(self.onClick)

    def onClick(self):
      """   print("Button Clicked")
        self.button.setText("Cliked!")
        self.button.setDisabled(True) """
      self.label0.setText("pushed")

    def submit(self):
        text = self.line_edit.text()
        print(f"Hello {text} ")
       

#begin the app
def main():
    #instanciation of app and windows
    app = QApplication(sys.argv)
    #sys.argv allows pyqt5 to process code line arguments
    window = MainWindow()
    window.show()
    #the windows are normally hiden
    sys.exit(app.exec_())
    #close the app when the user needs to

if __name__ == "__main__":
    main()
#verify if the file running is the main one