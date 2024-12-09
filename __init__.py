import os
import sys

# Add libs directory to Python path
libs_dir = os.path.join(os.path.dirname(__file__), 'libs')
if libs_dir not in sys.path:
    sys.path.append(libs_dir)

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, showWarning, getOnlyText
from anki.hooks import addHook
from anki.utils import stripHTML

from .src.ui.dialogs.sentence_dialog import SentenceDialog
from .src.ui.dialogs.article_dialog import GeneratedArticleDialog
from .src.ui.dialogs.config_dialog import ConfigDialog
from .src.utils.logger import Logger

class VocabMaster:
    """VocabMaster plugin main class"""
    
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.logger = Logger(__name__)
        self.setup_menu()
        
    def setup_menu(self):
        """Set up plugin menu"""
        # Create menu
        menu = QMenu('VocabMaster', mw)
        
        # Add menu items
        article_action = QAction('Generate Article', mw)
        article_action.triggered.connect(self.show_article_dialog)
        menu.addAction(article_action)
        
        sentence_action = QAction('Practice Sentences', mw)
        sentence_action.triggered.connect(self.show_sentence_dialog)
        menu.addAction(sentence_action)
        
        menu.addSeparator()
        
        config_action = QAction('Settings', mw)
        config_action.triggered.connect(self.show_config_dialog)
        menu.addAction(config_action)
        
        # Add menu to Anki
        mw.form.menubar.addMenu(menu)
        
    def show_article_dialog(self):
        """Show article generation dialog"""
        try:
            # Get words from reviewed cards
            words = self.get_selected_words()
            if not words:
                showInfo("No reviewed words found in the current deck.")
                return
                
            dialog = GeneratedArticleDialog(words, self.config_path, mw)
            dialog.exec()
        except Exception as e:
            self.logger.error(f"Error showing article dialog: {e}")
            showWarning(str(e))
            
    def show_sentence_dialog(self):
        """Show sentence practice dialog"""
        try:
            # Get words from reviewed cards
            words = self.get_selected_words()
            if not words:
                showInfo("No reviewed words found in the current deck.")
                return
                
            dialog = SentenceDialog(words, self.config_path, mw)
            dialog.exec()
        except Exception as e:
            self.logger.error(f"Error showing sentence dialog: {e}")
            showWarning(str(e))
            
    def get_selected_words(self) -> list[str]:
        """Get words from cards reviewed today in current deck"""
        from aqt import mw
        
        # 获取当前deck中已复习的卡片
        query = "deck:current rated:1"
        reviewed_cards = mw.col.find_cards(query)
        
        words = set()
        for card_id in reviewed_cards:
            card = mw.col.get_card(card_id)
            note = card.note()
            if note:
                word = stripHTML(note.fields[0])
                words.add(word)
        return list(words)
        
    def show_config_dialog(self):
        """Show configuration dialog"""
        try:
            dialog = ConfigDialog(self.config_path, mw)
            dialog.exec()
        except Exception as e:
            self.logger.error(f"Error showing config dialog: {e}")
            showWarning(str(e))

# Create plugin instance
vocab_master = VocabMaster()