def apply_dark_mode_style(widget):
    """Apply dark mode style to a widget"""
    widget.setStyleSheet("""
        QDialog {
            background-color: #3c3c3c;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #777777;
        }
        QTextEdit, QListWidget, QComboBox {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 8px;
        }
        QListWidget::item:selected {
            background-color: #3c3c3c;
            color: #e0e0e0;
        }
        QGroupBox {
            border: 1px solid #555555;
            border-radius: 4px;
            margin-top: 1em;
            padding-top: 0.5em;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
        }
    """)
