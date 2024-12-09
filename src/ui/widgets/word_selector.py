from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QCheckBox, QPushButton, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal

class WordSelector(QWidget):
    """Widget for selecting words from a list with checkboxes"""
    
    words_selected = pyqtSignal(list)  # Signal emitted when selection changes
    
    def __init__(self, words: list[str], parent=None):
        super().__init__(parent)
        self.words = sorted(words)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header with word count
        header = QLabel(f"Total words: {len(self.words)}")
        header.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(header)
        
        # Word list with checkboxes
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:hover {
                background-color: #E3F2FD;
            }
        """)
        
        for word in self.words:
            item = QListWidgetItem()
            self.list_widget.addItem(item)
            
            checkbox = QCheckBox(word)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.on_selection_changed)
            
            self.list_widget.setItemWidget(item, checkbox)
            
        layout.addWidget(self.list_widget)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        select_all = QPushButton("Select All")
        deselect_all = QPushButton("Deselect All")
        
        for btn in (select_all, deselect_all):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            
        select_all.clicked.connect(self.select_all)
        deselect_all.clicked.connect(self.deselect_all)
        
        btn_layout.addWidget(select_all)
        btn_layout.addWidget(deselect_all)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
    def select_all(self):
        """Select all words"""
        self._set_all_checked(True)
        
    def deselect_all(self):
        """Deselect all words"""
        self._set_all_checked(False)
        
    def _set_all_checked(self, checked: bool):
        """Set all checkboxes to checked/unchecked state"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            checkbox.setChecked(checked)
            
    def get_selected_words(self) -> list[str]:
        """Get list of selected words"""
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            if checkbox.isChecked():
                selected.append(checkbox.text())
        return selected
        
    def on_selection_changed(self):
        """Handle selection change"""
        self.words_selected.emit(self.get_selected_words())
