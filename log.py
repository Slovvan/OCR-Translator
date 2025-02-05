import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QTextEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QTextCursor
from googletrans import Translator
import nltk
import spacy
from nltk.wsd import lesk 
from nltk.corpus import wordnet
from tooltip import tooltipWindow
from cards import deckWindow

nlp = spacy.load("es_core_news_sm")

#nltk.download('punkt')
# Check if WordNet is already downloaded
""" try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')  # Multilingual WordNet """


class logWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.log_text = QTextEdit(self)
        self.log_text.setGeometry(0,0 , 300, 400)
        self.log_text.setReadOnly(True)
        self.log_text.viewport().installEventFilter(self)  # Install event filter on the QTextEdit viewport
        
        
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
        translation = self.translator.translate(text, src="auto", dest=self.desLang)
        return translation.text

    def get_synonyms_and_meanings(self, word):
        synonyms = set()
        meanings = []
        
        # Query WordNet for synsets using the specified language.
        synsets = wordnet.synsets(word, lang=self.orLang)
        for syn in synsets:
            # Add the lemma names (synonyms) to the set with a specified lang
            for lemma in syn.lemmas(self.orLang):
                synonyms.add(lemma.name()) # Add synonyms

                # Get the definition of the synset (meaning)
            meanings.append(self.translate(syn.definition()))
        
        # Limit the number of synonyms
        synonyms = list(synonyms)[:3]

        return synonyms, meanings

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

        # Return the result of the event filter to allow normal processing of other events
        return super().eventFilter(source, event)
    
    def selectLang(self, lang):
        if lang == "es":
            self.orlang = "spa"
        elif lang == "en":
            self.orlang = "eng"
        elif lang == "ja":
            self.orlang = "jpn"
        elif lang == "fr":
            self.orlang = "fra"
    


        

        
        

def main():
    app = QApplication(sys.argv)
    window = logWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

""" 
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from googletrans import Translator
import nltk
from nltk.corpus import wordnet

# Check if WordNet is already downloaded
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')  # Multilingual WordNet


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
        self.word_translations = {}  # Store word translations and details
        
    def add_text(self, text):
        # Original and translated sentence
        self.log_text.append(f"OCR text: {text}")

        translated = self.translate(text)
        self.log_text.append(f"Translated Text OCR: {translated} \n")

        # Add words with translations
        words = text.split()
        translated_words = self.translate_words(words)
        self.word_translations = translated_words  # Store for hover detection

        for word in words:
            self.log_text.insertPlainText(word + " ")

    def translate_words(self, words):
        translated_words = {}

        for word in words:
            # Get synonyms and meanings using WordNet
            synonyms, meanings = self.get_synonyms_and_meanings(word)
            
            # Translate the word to English for consistency
            translated_word = self.translate(word)
            
            # Translate the English synonyms to Spanish
            synonyms_es = [self.translate(synonym) for synonym in synonyms]

            translated_words[word] = {
                'translation': translated_word, 
                'synonyms': synonyms_es, 
                'meanings': meanings
            }

        return translated_words  # Return after processing all words

    def translate(self, text):
        translation = self.translator.translate(text, src="auto", dest="en")
        return translation.text

    def get_synonyms_and_meanings(self, word):
        # Get synonyms and meanings using NLTK WordNet
        synonyms = set()
        meanings = []
        
        # Get synsets for the word
        for syn in wordnet.synsets(word):
            # Add the lemma names (synonyms) to the set
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())  # Add synonyms

            # Get the definition of the synset (meaning)
            meanings.append(syn.definition())
        
        # Limit the number of synonyms
        synonyms = list(synonyms)[:3]
        
        return synonyms, meanings

    def eventFilter(self, source, event):
        # Check if the event is coming from the QTextEdit viewport and if it's a mouse move
        if source is self.log_text.viewport() and event.type() == event.MouseMove:
            # Get the text cursor at the mouse position
            cursor = self.log_text.cursorForPosition(event.pos())
            cursor.select(QTextCursor.WordUnderCursor)
            hovered_word = cursor.selectedText()

            # Verify if the selected word has a translation in self.word_translations
            if hovered_word in self.word_translations:
                translated_word = self.word_translations[hovered_word]['translation']
                synonyms = self.word_translations[hovered_word]['synonyms']
                meanings = self.word_translations[hovered_word]['meanings']
                
                # Construct the tooltip text
                tooltip_text = f"{hovered_word} -> {translated_word}\n"
                tooltip_text += f"Meaning (EN): {', '.join(meanings)}\n"
                tooltip_text += f"Synonyms (ES): {', '.join(synonyms) if synonyms else 'None'}"

                # Show tooltip with translated word
                QToolTip.showText(
                    event.globalPos(),  # Global position where the tooltip appears
                    tooltip_text, 
                    self.log_text,  # Associated widget of the tooltip
                )
            else:
                QToolTip.hideText()

        # Return the result of the event filter to allow normal processing of other events
        return super().eventFilter(source, event)

def main():
    app = QApplication(sys.argv)
    window = logWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
 """