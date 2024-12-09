from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QComboBox, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from .api_handler import APIHandler
import os
import json
from .loading_overlay import LoadingOverlay

class ConfigDialog(QDialog):
    config_updated = pyqtSignal()

    def __init__(self, config_path, parent=None):
        super().__init__(parent)
        self.config_path = config_path
        self.api_handler = APIHandler(config_path)
        self.rate_limit_timer = None
        self.loading_overlay = None
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        self.setWindowTitle("Vocab Master Settings")
        self.setWindowIcon(QIcon(':/icons/settings.png'))
        layout = QVBoxLayout()

        # API Settings Group
        api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()

        # API Type
        api_type_layout = QHBoxLayout()
        api_type_label = QLabel("API Type:")
        self.api_type_combo = QComboBox()
        self.api_type_combo.addItems(["OpenAI", "ChatGLM"])
        api_type_layout.addWidget(api_type_label)
        api_type_layout.addWidget(self.api_type_combo)
        api_layout.addLayout(api_type_layout)

        # API Key
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        api_layout.addLayout(api_key_layout)

        # Model Selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.update_model_list()  # Update model list based on selected API
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        api_layout.addLayout(model_layout)

        # Connect API type change to model list update
        self.api_type_combo.currentTextChanged.connect(self.update_model_list)

        # Test Connection Button
        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self.test_connection)
        api_layout.addWidget(self.test_button)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # Language Settings Group
        lang_group = QGroupBox("Language Settings")
        lang_layout = QVBoxLayout()

        # Target Language
        target_lang_layout = QHBoxLayout()
        target_lang_label = QLabel("Target Language:")
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems([
            "English", "Chinese", "Japanese", "Korean",
            "French", "German", "Spanish", "Italian",
            "Russian", "Portuguese", "Arabic"
        ])
        target_lang_layout.addWidget(target_lang_label)
        target_lang_layout.addWidget(self.target_lang_combo)
        lang_layout.addLayout(target_lang_layout)

        # Feedback Language
        feedback_lang_layout = QHBoxLayout()
        feedback_lang_label = QLabel("Feedback Language:")
        self.feedback_lang_combo = QComboBox()
        self.feedback_lang_combo.addItems([
            "English", "Chinese", "Japanese", "Korean",
            "French", "German", "Spanish", "Italian",
            "Russian", "Portuguese", "Arabic"
        ])
        feedback_lang_layout.addWidget(feedback_lang_label)
        feedback_lang_layout.addWidget(self.feedback_lang_combo)
        lang_layout.addLayout(feedback_lang_layout)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setIcon(QIcon(':/icons/save.png'))
        save_button.clicked.connect(self.save_config)
        cancel_button = QPushButton("Cancel")
        cancel_button.setIcon(QIcon(':/icons/cancel.png'))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_config(self):
        config = self.api_handler.config
        self.api_type_combo.setCurrentText(config.get("api_type", "OpenAI"))
        self.api_key_input.setText(config.get("api_key", ""))
        self.target_lang_combo.setCurrentText(config.get("target_language", "English"))
        self.feedback_lang_combo.setCurrentText(config.get("feedback_language", "English"))
        self.model_combo.setCurrentText(config.get("model", ""))

    def save_config(self):
        config = {
            "api_type": self.api_type_combo.currentText(),
            "api_key": self.api_key_input.text(),
            "target_language": self.target_lang_combo.currentText(),
            "feedback_language": self.feedback_lang_combo.currentText(),
            "model": self.model_combo.currentText()
        }
        try:
            self.api_handler.save_config(config)
            self.config_updated.emit()
            self.accept()
        except Exception as e:
            self.show_error("Failed to save configuration", str(e))

    def test_connection(self):
        self.test_button.setEnabled(False)
        self.status_label.setText("Testing connection...")
        self.status_label.setStyleSheet("color: blue;")
        self.show_loading_overlay("Testing connection...")
        
        try:
            api_type = self.api_type_combo.currentText()
            api_key = self.api_key_input.text()
            model = self.model_combo.currentText()
            
            if not api_key:
                raise ValueError("API key is required")
            
            success = self.api_handler.test_connection(api_type, api_key, model)
            
            if success:
                self.status_label.setText("Connection successful!")
                self.status_label.setStyleSheet("color: green;")
            else:
                self.status_label.setText("Connection failed. Please check your API key.")
                self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg:
                # Extract wait time if available
                import re
                wait_match = re.search(r"try again in (?:about )?(\d+) (\w+)", error_msg)
                if wait_match:
                    amount, unit = wait_match.groups()
                    self.status_label.setText(f"Rate limit reached. Please wait {amount} {unit}.")
                else:
                    self.status_label.setText("Rate limit reached. Please try again later.")
            else:
                self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
        finally:
            self.test_button.setEnabled(True)
            self.hide_loading_overlay()

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_loading_overlay(self, message="Testing connection..."):
        if not self.loading_overlay:
            self.loading_overlay = LoadingOverlay(self, message)
            self.loading_overlay.resize(self.size())
        self.loading_overlay.show()

    def hide_loading_overlay(self):
        if self.loading_overlay:
            self.loading_overlay.hide()

    def update_model_list(self):
        api_type = self.api_type_combo.currentText()
        if api_type == "OpenAI":
            self.model_combo.clear()
            self.model_combo.addItems(["gpt-3.5-turbo"])
        elif api_type == "ChatGLM":
            self.model_combo.clear()
            self.model_combo.addItems(["glm-4"])

    def closeEvent(self, event):
        if self.rate_limit_timer and self.rate_limit_timer.isActive():
            self.rate_limit_timer.stop()
        super().closeEvent(event)
