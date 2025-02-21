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
import requests
from janome.tokenizer import Tokenizer

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

        # Initialize Janome tokenizer for Japanese segmentation
        self.tokenizer = Tokenizer()

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
        # words = text.split()
        words = self.tokenize_japanese_text(text)  # Use Janome for better segmentation
        self.translate_words(words)
        

        for word in words:
            self.log_text.insertPlainText(word + " ")

    def tokenize_japanese_text(self, text):
        # Use Janome tokenizer to break the Japanese text into words
        tokens = self.tokenizer.tokenize(text)
        return [token.surface for token in tokens]


    def translate_words(self, words):
        for word in words:
            # Get synonyms and meanings using WordNet and giving a specified lang
            word_form, reading, synonyms, meanings = self.get_synonyms_and_meanings(word)

            # Translate the word for consistency
            translated_word = self.translate(word)

            #store for hover detection
            self.word_translations[word] = {
                'translation': translated_word,
                'word_form': word_form,
                'reading': reading,
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
    
    def lookup_jisho(self, word):
        url = "https://jisho.org/api/v1/search/words"
        params = {"keyword": word}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("data"):
                first_result = data["data"][0]
                japanese_entry = first_result["japanese"][0]
                word_form = japanese_entry.get("word", "")  # Kanji form if present.
                reading = japanese_entry.get("reading", "")
                senses = first_result.get("senses", [])
                meanings = []
                for sense in senses:
                    meanings.extend(sense.get("english_definitions", []))
                return {
                    "word": word_form,
                    "reading": reading,
                    "meanings": meanings
                }
        except Exception as e:
            print("Error looking up Jisho:", e)
        return None

    def get_synonyms_and_meanings(self, word):
        synonyms = set()
        meanings = []

        cleaned_word = self.clean_word(word)

        # If the language is Japanese, use Jisho lookup.
        if self.orLang == "jpn":
            jisho_data = self.lookup_jisho(cleaned_word)
            if jisho_data:
                print(jisho_data)
                
                word = jisho_data.get("word", word),
                reading = jisho_data.get("reading", ""),
                synonyms = [] # Jisho doesn't return synonyms
                meanings = jisho_data.get("meanings", [])
                return word, reading, synonyms, meanings
            
            else:
                return [], [], [], []
            
            
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
        """ {
        "word": word,
        "reading": "",
        "synonyms": synonyms,
        "meanings": meanings
        } """

        return [], [], synonyms, meanings
    
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
       
                    word_form = self.word_translations[hovered_word]['word_form']
                    reading = self.word_translations[hovered_word]['reading']

                    info = {
                        "word": hovered_word,
                        "translation": translated_word,
                        "synonyms": synonyms,
                        "meanings": meanings,
                        "position": position,
                        "word_form": meanings,
                        "reading": reading,
                        "lang": self.orLang
                        
                    }
                    if self.orLang == "jpn":
                        info["word_form"] = word_form
                        info["reading"] = reading

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

    def update_tooltip(self, word, label):
        word_data = self.get_synonyms_and_meanings(word)

        if word_data:
            word_text = word_data.get("word", word)
            reading = word_data.get("reading", "")
            synonyms = word_data.get("synonyms", [])
            meanings = word_data.get("meanings", [])

            # Construct tooltip text dynamically
            tooltip_text = f"<b>{word_text}</b>"
            if reading:
                tooltip_text += f" ({reading})"

            if meanings:
                tooltip_text += "<br><b>Meanings:</b><ul>"
                for meaning in meanings:
                    tooltip_text += f"<li>{meaning}</li>"
                tooltip_text += "</ul>"

            if synonyms:
                tooltip_text += "<br><b>Synonyms:</b> " + ", ".join(synonyms)

            label.setToolTip(tooltip_text)  # Set tooltip to QLabel


    


def main():
    app = QApplication(sys.argv)
    window = logWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

