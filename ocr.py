import sys
import cv2
import keyboard
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QEvent, QObject, QRect, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QScreen
from PIL import ImageGrab, Image
from log import logWindow
import unicodedata


import numpy as np

class OcrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ocr")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        

        self.UI()
        #to save mouse position
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        self.is_resizing = False
        self.resize_margin = 10  # Define margin for resizing window            こんにちは  

        #selected lang
        self.lang = "spa"

        #instance of logwindow and ocrwindow instance as argument to use it in logwindow
        self.log_window = logWindow(self) 

        #the keyboard module runs in a different thread from QT 
        #Use of QTimer to call screenShot() in the main GUI thread
        keyboard.add_hotkey(".+-", lambda: QTimer.singleShot(0, self.screenShot))

    def UI(self):
        widget_style = "border-color: rgba(255, 0, 0, 255);" \
                       "border-style: solid;" \
                       "border-width: 2px;" \
                       "border-radius: 2px;" \
                       "background-color: rgba(255, 255, 255, 2);"
    

        #Create a box widget
        cLayout = QWidget(self)
        cLayout.setStyleSheet(widget_style)
        cLayout.setMouseTracking(True)
        cLayout.installEventFilter(self)
       
        #set window with the new box window
        self.setCentralWidget(cLayout)

    #change icon of mouse when it is released
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.is_resizing = False


    #changes coordenates to move window later
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos_x = event.pos().x()
            self.mouse_pos_y = event.pos().y()
        
         # Check if it's within the resize area
        if (self.width() - event.pos().x() <= self.resize_margin) or (self.height() - event.pos().y() <= self.resize_margin):
            self.is_resizing = True
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)  # Resize cursor

    #move window
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
          # Only process mouse move events
        if event.type() == QEvent.MouseMove:
            if self.is_resizing:
                # Resize window based on mouse movement
                dx = event.pos().x() - self.mouse_pos_x
                dy = event.pos().y() - self.mouse_pos_y
                self.resize(self.width() + dx, self.height() + dy)
                self.mouse_pos_x = event.pos().x()
                self.mouse_pos_y = event.pos().y()
            elif event.buttons() & Qt.LeftButton:
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                self.move(event.globalPos().x() - self.mouse_pos_x,
                        event.globalPos().y() - self.mouse_pos_y)
            return True  # We handled the event
        else:
            return False

    #Send text captured to log
    def SendText(self, img):
        #transform pil image into cv for preprocessing
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # Convert PIL to OpenCV (BGR)

        processed = self.morphological_operations(img_cv2)  #Separate text in rows

        pil_image = Image.fromarray(processed)  # Convert back to PIL for Tesseract
        ocr_result = pytesseract.image_to_string(pil_image,  lang=self.lang, config='--psm 1')
        ocr3 = pytesseract.image_to_string(pil_image,  lang=self.lang, config='--psm 3')
        ocr4 = pytesseract.image_to_string(pil_image,  lang=self.lang, config='--psm 4')
        ocr5 = pytesseract.image_to_string(pil_image,  lang=self.lang, config='--psm 5')
        ocr6 = pytesseract.image_to_string(pil_image,  lang=self.lang, config='--psm 6')
        """ print(ocr_result)
        print(ocr3)
        print(ocr4)
        print(ocr5) """
        print(ocr6)
        
        if ocr6 == "":
            print("There is no text")
        else:
            if self.log_window:
                if self.lang == "jpn":
                    grouped_words = self.group_japanese_text(ocr6)
                    print(grouped_words)
                    self.log_window.add_text(grouped_words)
                else:
                    self.log_window.add_text(ocr6)
         
                self.log_window.show()
       
    
    def screenShot(self):
        # get geometry of the central widget without borders
        widget_geom = self.centralWidget().geometry()

        #Turn local coordenates from the central widget to global
        topLeft = self.centralWidget().mapToGlobal(widget_geom.topLeft())
        bottomRight = self.centralWidget().mapToGlobal(widget_geom.bottomRight())

        # get coordenates from the screen
        x1, y1 = topLeft.x(), topLeft.y()
        x2, y2 = bottomRight.x(), bottomRight.y()

        # screenshot insede the limits
        im = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        ocr_text = self.SendText(im)

    
    def morphological_operations(self, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # Define a small kernel
        processed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)  # Apply closing to fill gaps
        return processed

   
    def group_japanese_text(self, text):
        """
        Group characters into words based on common Japanese language patterns.
        This approach assumes characters are output from OCR and are separated.
        """
        words = []
        current_word = []
        
        # Loop through each character in the OCR output
        for char in text:
            # Check if the character is part of a Japanese word
            if unicodedata.category(char) in ['Lo', 'Lm']:  # Lo -> Letter, Other; Lm -> Modifier Letters (mostly part of words)
                current_word.append(char)
            else:
                # If we encounter a non-letter, end the current word and start a new one
                if current_word:
                    words.append(''.join(current_word))  # Join the characters to form a word
                    current_word = []  # Reset for the next word
                
                # Add punctuation or spaces as individual "words" or tokens
                if char.strip():
                    words.append(char)

        # Append the last word if there is one
        if current_word:
            words.append(''.join(current_word))

        return ''.join(words)
    
    def selectLang(self, lang):
        if lang == "es":
            self.lang = "spa"
        elif lang == "en":
            self.lang = "eng"
        elif lang == "ja":
            self.lang = "jpn"
        elif lang == "fr":
            self.lang = "fra"


def main():
    app = QApplication(sys.argv)
    window = OcrWindow()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()