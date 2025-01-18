import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QToolTip, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from googletrans import Translator

class logWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log")
        self.setGeometry(500, 600, 300, 400)
        
        self.initUI()
        self.translator = Translator()
    
    def initUI(self):
        self.log_text = QTextEdit(self)
        self.log_text.setGeometry(0,0 , 300, 400)
        self.log_text.setReadOnly(True)
        self.log_text.viewport().installEventFilter(self)  # Install event filter on the QTextEdit viewport
        self.word_translations = {} 
        


    def add_text(self, text):
        #original and translated sentence
        self.log_text.append(f"Ocr text: {text}")

        translated = self.translate(text)
        self.log_text.append(f"Translated Text OCR: {translated} ")

       # Add words with translations
        words = text.split()
        translated_words = self.translate_words(words)
        self.word_translations = translated_words  # Store for hover detection
        for word in words:
            self.log_text.insertPlainText(word + " ")

    def translate_words(self,words):
        translated_words = {}

        for word in words:
            translation = self.translate(word)
            translated_words[word] = translation
        
        return translated_words


    def translate(self, text):
        
        translation = self.translator.translate(text, src="es", dest="en")

        return translation.text
    
    def eventFilter(self, source, event):
        #Verify if the event is comming from the QTextEdit viewport and if its a mouse one
        if source is self.log_text.viewport() and event.type() == event.MouseMove:
            #Gets the text cursor on the position of the mouse
            cursor = self.log_text.cursorForPosition(event.pos())
            
            cursor.select(QTextCursor.WordUnderCursor)
            hovered_word = cursor.selectedText()

            #Verify if the selected word has a translation in self.word_translation
            if hovered_word in self.word_translations:
                translated_word = self.word_translations[hovered_word]
                #Show toolTip with translated word
                QToolTip.showText(
                    event.globalPos(),  # mouse Global position where it appears
                    f"{hovered_word} -> {translated_word}", 
                    self.log_text,  # asociated Widget of the ToolTip
                )
            else:
                QToolTip.hideText()
        
        #Returns the result of the metod eventFilter, allowing the normal processing of other events
        return super().eventFilter(source, event)

    




def main():
    app = QApplication(sys.argv)
    window = logWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

