import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QTextCursor
from googletrans import Translator
import nltk
import spacy
from nltk.wsd import lesk 
from nltk.corpus import wordnet
from tooltip import tooltipWindow
from cards import deckWindow
import re

nlp = spacy.load("es_core_news_sm")

#nltk.download('punkt')
# Check if WordNet is already downloaded
""" try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')  # Multilingual WordNet """


class logWindow(QMainWindow):
    def __init__(self, ocr_window=None):
        super().__init__()
        self.ocr_window = ocr_window
        self.setWindowTitle("Log")
        self.setGeometry(500, 600, 300, 400)
        self.initUI()
        self.translator = Translator()
        
        self.deck = deckWindow()
        self.tooltip = tooltipWindow()
        self.stayOpen = False
        self.translated_phrase = ""  # store complete translations
        self.word_translations = {}  # Store word translations and details
        self.words_in_deck = []
        
        self.orLang = "spa"
        self.desLang = "en"

    def initUI(self):
        #main layout
        layout = QVBoxLayout()

        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"
        
        #create widget to store all the text
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.log_text.viewport().installEventFilter(self)  # Install event filter on the QTextEdit viewport
        layout.addWidget(self.log_text)


         # Instance of a button to close
        capture_button = QPushButton("Capture")
        capture_button.setFixedSize(85, 30)
        capture_button.setStyleSheet(button_style)

        #capture text
        if self.ocr_window:
            capture_button.clicked.connect(self.ocr_window.screenShot)#click events do not have parenthesis 

        close_button = QPushButton("Close")
        close_button.setFixedSize(85, 30)
        close_button.setStyleSheet(button_style)

        #close window
        if self.ocr_window:
            close_button.clicked.connect(self.ocr_window.close) 

        #horizontal layout for buttons
        buttons = QHBoxLayout()
        buttons.addWidget(capture_button)
        buttons.addWidget(close_button)

        #add the buttons to the main layout
        layout.addLayout(buttons)

        #central layout to add the new created layout to the main window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        
    def add_text(self, text):
        #empty phrase to avoid giving previous text 
        self.translated_phrase = ""
        # Original and translated sentence
        self.log_text.append(f"OCR text: {text}")

        self.translated_phrase = self.translate(text)
        self.log_text.append(f"Translated Text OCR: {self.translated_phrase} \n")

        # Add words with translations
        words = text.split()
        self.translate_words(words)
        

        for word in words:
            self.log_text.insertPlainText(word + " ")


    def translate_words(self, words):
        for word in words:
            # Get synonyms and meanings using WordNet and giving a specified lang
            synonyms, meanings = self.get_synonyms_and_meanings(word)
            
            # Translate the word to English for consistency
            translated_word = self.translate(word)
            
            #store for hover detection
            self.word_translations[word] = {
                'translation': translated_word, 
                'synonyms': synonyms, 
                'meanings': meanings
            }

        return self.word_translations  # Return after processing all words

    def translate(self, text): 
        try:       
            translation = self.translator.translate(text, src="auto", dest=self.desLang)
            return translation.text
        except Exception as e:
            print("Translation error: ", e)

    def get_synonyms_and_meanings(self, word):
        synonyms = set()
        meanings = []

        cleaned_word = self.clean_word(word)
        print(cleaned_word)
        # Query WordNet for synsets using the specified language.
        synsets = wordnet.synsets(cleaned_word, lang=self.orLang)
        for syn in synsets:
            # Add the lemma names (synonyms) to the set with a specified lang
            for lemma in syn.lemmas(self.orLang):
                synonyms.add(lemma.name()) # Add synonyms

                # Get the definition of the synset (meaning)
            meanings.append(self.translate(syn.definition()))
        
        # Limit the number of synonyms
        synonyms = list(synonyms)[:3]

        return synonyms, meanings
    
    def clean_word(self, word):
        # Keep only letters (including accents), numbers, hyphens, and apostrophes
        cleaned = re.sub(r"[^\w\s'-]", "", word)  
        return cleaned.strip()

    def eventFilter(self, source, event):
        # Check if the event is coming from the QTextEdit viewport and if it's a mouse move
        if source is self.log_text.viewport():
            
            if event.type() == event.MouseMove:
                # Get the text cursor at the mouse position
                cursor = self.log_text.cursorForPosition(event.pos())
                cursor.select(QTextCursor.WordUnderCursor)
                hovered_word = cursor.selectedText()
            

                # Verify if the selected word has a translation in self.word_translations
                if hovered_word in self.word_translations:
                    translated_word = self.word_translations[hovered_word]['translation']
                    synonyms = self.word_translations[hovered_word]['synonyms']
                    meanings = self.word_translations[hovered_word]['meanings']
                    position = self.mapToGlobal(event.pos()) + QPoint(10, 10)

                    info = {
                        "word": hovered_word,
                        "translation": translated_word,
                        "synonyms": synonyms,
                        "meanings": meanings,
                        "position": position
                    }

                    self.tooltip.saveInfo(info)

                #hide window if a word is not being hovered
                else:
                    self.tooltip.hide()

            if event.type() == event.MouseButtonPress:

                cursor = self.log_text.cursorForPosition(event.pos())
                cursor.select(QTextCursor.WordUnderCursor)
                clicked_word = cursor.selectedText()

                if clicked_word in self.words_in_deck:
                    print("Word already in deck")
                else:
                    self.deck.createCard(clicked_word, self.translated_phrase)
                    self.words_in_deck.append(clicked_word)
                
                # Construct the tooltip text
                """ tooltip_text = f"{hovered_word} -> {translated_word}\n"
                tooltip_text += f"Meaning (EN): {', '.join(meanings)}\n"
                tooltip_text += f"Synonyms (ES): {', '.join(synonyms) if synonyms else 'None'}" """

                # Show tooltip with translated word
                """    QToolTip.showText(
                    event.globalPos(),  # Global position where the tooltip appears
                    tooltip_text, 
                    self.log_text,  # Associated widget of the tooltip
                ) """
                #QToolTip.hideText()
                 # Hide tooltip if mouse leaves QTextEdit completely

        # Return the result of the event filter to allow normal processing of other events
        return super().eventFilter(source, event)
    
    def selectLang(self, lang):
        if lang == "es":
            self.orLang = "spa"
        elif lang == "en":
            self.orLang = "eng"
        elif lang == "ja":
            self.orLang = "jpn"
        elif lang == "fr":
            self.orLang = "fra"

def main():
    app = QApplication(sys.argv)
    window = logWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

