from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor

class LoadingOverlay(QWidget):
    """Loading overlay widget with animated dots"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.dot_count = 0
        self.timer = None
        self.setup_ui()

    def setup_ui(self):
        """Set up the overlay UI"""
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
            }
            QLabel {
                color: #c8c8c8;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        self.loading_label = QLabel("Loading")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)
        self.setLayout(layout)

    def enhance_loading_animation(self):
        """Start the loading animation"""
        if self.timer is None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_dots)
            self.timer.start(500)

    def update_dots(self):
        """Update the loading dots animation"""
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.loading_label.setText(f"Loading{dots}")

    def paintEvent(self, event):
        """Custom paint event for the overlay"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 30, 180))

    def show(self):
        """Show the overlay and start animation"""
        if self.parent:
            self.resize(self.parent.size())
        self.enhance_loading_animation()
        super().show()
        self.raise_()

    def hide(self):
        """Hide the overlay and stop animation"""
        if self.timer:
            self.timer.stop()
            self.timer = None
        super().hide()

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        if self.parent:
            self.resize(self.parent.size())
