from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal

class WordComboBox(QComboBox):
    """Combobox for selecting a single word"""
    
    word_selected = pyqtSignal(str)  # Signal emitted when word is selected
    
    def __init__(self, words: list[str], parent=None):
        super().__init__(parent)
        self.addItems(sorted(words))
        self.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.currentTextChanged.connect(self.word_selected.emit)
