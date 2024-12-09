from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTextEdit, QComboBox, QGroupBox, QWidget, QSplitter
)
from PyQt6.QtCore import Qt
from ...api.api_handler import APIHandler
from ...utils.worker import AIWorker
from ..widgets.word_combobox import WordComboBox
from ..widgets.loading_overlay import LoadingOverlay
from ..styles.dark_mode import apply_dark_mode_style
import time
from PyQt6.QtWidgets import QApplication
from aqt import mw
import markdown2
class SentenceDialog(QDialog):
    def __init__(self, words, config_path, parent=None):
        super().__init__(parent)
        self.words = words
        self.api_handler = APIHandler(config_path)
        self.loading_overlay = None
        self.worker = None
        self.night_mode = self.is_night_mode()
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        self.setWindowTitle("Practice Sentences")
        self.setMinimumSize(800, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        # Loading overlay
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.hide()
        
        if self.night_mode:
            apply_dark_mode_style(self)
            
        self.setup_layout()
        self.load_words()
        
    def setup_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout.addWidget(self.create_instructions())
        main_layout.addWidget(self.create_word_selection())
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setChildrenCollapsible(False)
        
        splitter.addWidget(self.create_sentence_section())
        splitter.addWidget(self.create_feedback_section())
        splitter.addWidget(self.create_examples_section())
        
        splitter.setSizes([150, 200, 150])
        main_layout.addWidget(splitter)
        
        self.setLayout(main_layout)
        
    def create_instructions(self):
        instructions = QLabel(
            "1. Select or type a word\n"
            "2. Write a sentence using that word\n"
            "3. Click 'Evaluate' to get feedback\n"
            "4. Click 'Show Examples' to see example sentences"
        )
        instructions.setMaximumHeight(80)
        return instructions
        
    def create_word_selection(self):
        word_group = QGroupBox("Select Word")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.word_combo = WordComboBox(self.words)
        self.word_combo.word_selected.connect(self.on_word_selected)
        layout.addWidget(self.word_combo)
        
        word_group.setLayout(layout)
        word_group.setMaximumHeight(80)
        return word_group
        
    def create_sentence_section(self):
        group = QGroupBox("Your Sentence")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.sentence_input = QTextEdit()
        self.sentence_input.setPlaceholderText("Type your sentence here...")
        self.sentence_input.setMinimumHeight(50)
        self.sentence_input.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled)
        self.sentence_input.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.sentence_input.raise_()
        
        container_layout.addWidget(self.sentence_input)
        layout.addWidget(container)
        
        self.evaluate_btn = QPushButton("Evaluate")
        layout.addWidget(self.evaluate_btn)
        
        group.setLayout(layout)
        return group
        
    def create_feedback_section(self):
        group = QGroupBox("Feedback")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setMinimumHeight(50)
        self.feedback_text.setPlaceholderText("Feedback will appear here...")
        
        layout.addWidget(self.feedback_text)
        group.setLayout(layout)
        return group
        
    def create_examples_section(self):
        group = QGroupBox("Example Sentences")
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.example_text = QTextEdit()
        self.example_text.setReadOnly(True)
        self.example_text.setMinimumHeight(50)
        self.example_text.setPlaceholderText("Example sentences will appear here...")
        layout.addWidget(self.example_text)
        
        self.examples_btn = QPushButton("Show Examples")
        layout.addWidget(self.examples_btn)
        
        group.setLayout(layout)
        return group
        
    def setup_connections(self):
        self.evaluate_btn.clicked.connect(self.evaluate_sentence)
        self.examples_btn.clicked.connect(self.show_examples)
        
    def evaluate_sentence(self):
        sentence = self.sentence_input.toPlainText().strip()
        word = self.word_combo.currentText().strip()
        
        if not sentence or not word:
            return
            
        self.start_worker("evaluate_sentence", {
            "sentence": sentence,
            "target_word": word
        })
        
    def show_examples(self):
        word = self.word_combo.currentText().strip()
        if not word:
            return
            
        self.start_worker("generate_examples", {
            "word": word,
            "count": 3
        })
        
    def start_worker(self, action, params):
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait()
            
        self.worker = AIWorker(action, params, self.api_handler.config_path)
        self.worker.finished.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)
        self.worker.rate_limit.connect(self.handle_rate_limit)
        self.worker.result_ready.connect(self.on_chunk_received)
        self.loading_overlay.show()
        self.worker.start()
        
    def handle_result(self, result):
        if self.worker.action == "evaluate_sentence":
            self.feedback_text.clear()
            html = markdown2.markdown(result)
            self.feedback_text.setHtml(f"<div style='font-family: Georgia, serif; font-size: 16px;'>{html}</div>")
        elif self.worker.action == "generate_examples":
            self.example_text.clear()
            html = markdown2.markdown(result)
            self.example_text.setHtml(f"<div style='font-family: Georgia, serif; font-size: 16px;'>{html}</div>")
        QApplication.processEvents()  # Update UI
        self.loading_overlay.hide() 

                
    def handle_error(self, error_msg):
        from aqt.utils import showWarning
        showWarning(f"Error: {error_msg}")
        self.loading_overlay.hide() 
        
    def handle_rate_limit(self, message, wait_time):
        from aqt.utils import showWarning
        showWarning(f"Rate limit exceeded. Please wait {wait_time} seconds and try again.")
        
    def load_words(self):
        # Implementation remains the same
        pass
        
    def is_night_mode(self):
        """Check if night mode is enabled using theme manager"""
        try:
            return mw.theme_manager.night_mode
        except:
            return False
        
    def on_word_selected(self, word: str):
        """Handle word selection change"""
        self.evaluate_btn.setEnabled(bool(word))
        
    def on_chunk_received(self, chunk: str):
        """Handle receiving a chunk of generated text"""
        ...
