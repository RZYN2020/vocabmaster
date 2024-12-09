from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QApplication
)
from PyQt6.QtCore import Qt

from ...api.api_handler import APIHandler
from ...utils.worker import AIWorker
from ..widgets.loading_overlay import LoadingOverlay
from ..widgets.word_selector import WordSelector
from ..styles.dark_mode import apply_dark_mode_style
import markdown2

class GeneratedArticleDialog(QDialog):
    """Dialog for displaying AI-generated articles"""
    
    def __init__(self, words: list[str], config_path: str, parent=None):
        super().__init__(parent)
        self.words = words
        self.api_handler = APIHandler(config_path)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Generate Article")
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Word selector
        self.word_selector = WordSelector(self.words)
        self.word_selector.words_selected.connect(self.on_words_selected)
        layout.addWidget(self.word_selector)
        
        # Article display
        self.article_text = QTextEdit()
        self.article_text.setReadOnly(True)
        self.article_text.setPlaceholderText("Article will appear here...")
        layout.addWidget(self.article_text)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate_article)
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Loading overlay
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.hide()
        
        # Apply dark mode if enabled
        apply_dark_mode_style(self)
        
    def generate_article(self):
        """Generate article using selected words"""
        selected_words = self.word_selector.get_selected_words()
        if not selected_words:
            return
            
        self.article_text.clear()
        # self.loading_overlay.show()
        self.generate_btn.setEnabled(False)
        
        # Create worker for async generation
        self.worker = AIWorker(
            "generate_article",
            {"words": selected_words},
            self.api_handler.config_path
        )
        self.worker.result_ready.connect(self.on_chunk_received)
        self.worker.error.connect(self.handle_error)
        self.worker.finished.connect(self.handle_result)
        self.worker.rate_limit.connect(self.handle_rate_limit)
        self.loading_overlay.show()
        self.worker.start()
    
    def handle_rate_limit(self, message, wait_time):
        from aqt.utils import showWarning
        showWarning(f"Rate limit exceeded. Please wait {wait_time} seconds and try again.")
        
    def on_chunk_received(self, chunk: str):
        """Handle receiving a chunk of generated text"""
        ...
        
    def handle_result(self, result):
        """Handle completion of article generation"""
        self.loading_overlay.hide()
        html = markdown2.markdown(result)
        self.article_text.setHtml(f"<div style='font-family: Georgia, serif; font-size: 16px;'>{html}</div>")
        self.generate_btn.setEnabled(True)
        
    def handle_error(self, error_msg: str):
        """Handle generation error"""
        self.article_text.setPlainText(f"Error: {error_msg}")
        self.loading_overlay.hide()
        self.generate_btn.setEnabled(True)
        
    def on_words_selected(self, words: list[str]):
        """Handle word selection change"""
        self.generate_btn.setEnabled(bool(words))
