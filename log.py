import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QToolTip, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from googletrans import Translator
from textblob import Word

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
        self.log_text.append(f"Translated Text OCR: {translated} \n")

       # Add words with translations
        words = text.split()
        translated_words = self.translate_words(words)
        self.word_translations = translated_words  # Store for hover detection
        for word in words:
            self.log_text.insertPlainText(word + " ")

    def translate_words(self,words):
          translated_words = {}

          for word in words:
                # Translate the word to English first to get meaningful synonyms
                translated_word = self.translate(word)
                blob = Word(translated_word)
                lemma = blob.lemmatize()  # Use the core meaning of words
                
                # Get synonyms and meanings in English
                word_obj = Word(lemma)
                synonyms = word_obj.synsets
                meanings = [syn.definition() for syn in synonyms]
                
                # Translate synonyms back to Spanish
                synonyms_es = []
                for syn in synonyms[:3]:  # Limit the number of synonyms
                    synonym = syn.name().split('.')[0]  # Get the word without part of speech
                    synonyms_es.append(self.translator.translate(synonym, src="en", dest="es").text)

                translated_words[word] = {
                    'translation': translated_word, 
                    'synonyms': synonyms_es, 
                    'meanings': meanings
                }
            
                return translated_words

    def translate(self, text):
        translation = self.translator.translate(text, src="auto", dest="en")

        return translation.text

    def get_meaning_in_english(self, word):
        try:
            word_obj = Word(word)
            synonyms = word_obj.synsets  # Get synsets (related to meanings)
            meanings = [syn.definition() for syn in synonyms]
            return meanings[0] if meanings else "No definition found"
        except Exception as e:
            return "No definition found"

    def get_synonyms_in_spanish(self, word):
        try:
            word_obj = Word(word)
            synonyms = word_obj.synsets  # Get synsets
            synonym_words = set()

            for syn in synonyms:
                for lemma in syn.lemmas():
                    # Translate each synonym to Spanish
                    translated_synonym = self.translate(lemma.name())
                    synonym_words.add(translated_synonym.lower())

            return list(synonym_words) if synonym_words else ["No synonyms found"]
        except Exception as e:
            return ["No synonyms found"]
        
    def eventFilter(self, source, event):
        #Verify if the event is comming from the QTextEdit viewport and if its a mouse one
        if source is self.log_text.viewport() and event.type() == event.MouseMove:
            #Gets the text cursor on the position of the mouse
            cursor = self.log_text.cursorForPosition(event.pos())
            
            cursor.select(QTextCursor.WordUnderCursor)
            hovered_word = cursor.selectedText()

            #Verify if the selected word has a translation in self.word_translation
            if hovered_word in self.word_translations:
                translated_word = self.word_translations[hovered_word]['translation']
                synonyms = self.word_translations[hovered_word]['synonyms']
                meaning = self.word_translations[hovered_word]['meanings']
                
                # Construct the tooltip text
                tooltip_text = f"{hovered_word} -> {translated_word}\nSynonyms: "
                tooltip_text = f"{hovered_word} -> Meaning (EN): {meaning}\nSynonyms (ES): "
                tooltip_text += ", ".join(synonyms) if synonyms else "None"


                #Show toolTip with translated word
                QToolTip.showText(
                    event.globalPos(),  # mouse Global position where it appears
                    tooltip_text, 
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

