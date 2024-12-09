from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QComboBox, QGroupBox, QFormLayout,
    QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt

from ...api.api_handler import APIHandler
from ...config.config_manager import ConfigManager
from ..styles.dark_mode import apply_dark_mode_style

class ConfigDialog(QDialog):
    """Configuration dialog for VocabMaster settings"""

    def __init__(self, config_path: str, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager(config_path, validate=False)
        self.api_handler = APIHandler(config_path)
        
        self.setWindowTitle("VocabMaster Settings")
        self.setMinimumWidth(500)
        
        if self.is_night_mode():
            apply_dark_mode_style(self)
            
        self.setup_ui()

    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # API Settings
        api_group = self.create_api_settings()
        layout.addWidget(api_group)
        
        # Language Settings
        lang_group = self.create_language_settings()
        layout.addWidget(lang_group)
        
        # Advanced Settings
        adv_group = self.create_advanced_settings()
        layout.addWidget(adv_group)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        test_btn = QPushButton("Test Connection")
        button_box.addButton(test_btn, QDialogButtonBox.ButtonRole.ActionRole)
        
        button_box.accepted.connect(self.save_config)
        button_box.rejected.connect(self.reject)
        test_btn.clicked.connect(self.test_connection)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        self.load_current_config()

    def create_api_settings(self) -> QGroupBox:
        """Create API settings group"""
        group = QGroupBox("API Settings")
        layout = QFormLayout()
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(['OpenAI', 'ChatGLM'])
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        
        self.openai_key = QLineEdit()
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key.setPlaceholderText("Enter your OpenAI API key")
        
        self.chatglm_key = QLineEdit()
        self.chatglm_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.chatglm_key.setPlaceholderText("Enter your ChatGLM API key")
        
        self.model_combo = QComboBox()
        
        layout.addRow("API Provider:", self.provider_combo)
        layout.addRow("OpenAI API Key:", self.openai_key)
        layout.addRow("ChatGLM API Key:", self.chatglm_key)
        layout.addRow("Model:", self.model_combo)
        
        group.setLayout(layout)
        return group

    def create_language_settings(self) -> QGroupBox:
        """Create language settings group"""
        group = QGroupBox("Language Settings")
        layout = QFormLayout()
        
        self.target_lang = QComboBox()
        self.target_lang.addItems(['English', 'Chinese', 'Japanese', 'Korean', 
                                 'French', 'German', 'Spanish'])
        
        self.feedback_lang = QComboBox()
        self.feedback_lang.addItems(['English', 'Chinese', 'Japanese', 'Korean',
                                   'French', 'German', 'Spanish'])
        
        layout.addRow("Target Language:", self.target_lang)
        layout.addRow("Feedback Language:", self.feedback_lang)
        
        group.setLayout(layout)
        return group

    def create_advanced_settings(self) -> QGroupBox:
        """Create advanced settings group"""
        group = QGroupBox("Advanced Settings")
        layout = QFormLayout()
        
        self.temperature = QLineEdit()
        self.temperature.setPlaceholderText("0.0 - 1.0")
        
        self.max_retries = QLineEdit()
        self.max_retries.setPlaceholderText("Number of retries")
        
        self.retry_delay = QLineEdit()
        self.retry_delay.setPlaceholderText("Delay in seconds")
        
        self.timeout = QLineEdit()
        self.timeout.setPlaceholderText("Timeout in seconds")
        
        layout.addRow("Temperature:", self.temperature)
        layout.addRow("Max Retries:", self.max_retries)
        layout.addRow("Retry Delay:", self.retry_delay)
        layout.addRow("Timeout:", self.timeout)
        
        group.setLayout(layout)
        return group

    def on_provider_changed(self, provider: str):
        """Handle API provider change"""
        self.model_combo.clear()
        if provider == 'OpenAI':
            self.model_combo.addItems(['gpt-3.5-turbo', 'gpt-4'])
            self.openai_key.setEnabled(True)
            self.chatglm_key.setEnabled(False)
        else:
            self.model_combo.addItems(['glm-3', 'glm-4'])
            self.openai_key.setEnabled(False)
            self.chatglm_key.setEnabled(True)

    def load_current_config(self):
        """Load current configuration into UI"""
        config = self.config_manager
        
        # API Settings
        self.provider_combo.setCurrentText(config.get('api_provider'))
        self.openai_key.setText(config.get('openai_api_key'))
        self.chatglm_key.setText(config.get('chatglm_api_key'))
        
        if config.get('api_provider') == 'OpenAI':
            self.model_combo.setCurrentText(config.get('openai_model'))
        else:
            self.model_combo.setCurrentText(config.get('chatglm_model'))
        
        # Language Settings
        self.target_lang.setCurrentText(config.get('target_language'))
        self.feedback_lang.setCurrentText(config.get('feedback_language'))
        
        # Advanced Settings
        self.temperature.setText(str(config.get('temperature')))
        self.max_retries.setText(str(config.get('max_retries')))
        self.retry_delay.setText(str(config.get('retry_delay')))
        self.timeout.setText(str(config.get('timeout')))

    def get_config_updates(self) -> dict:
        """Get updated configuration values"""
        updates = {
            'api_provider': self.provider_combo.currentText(),
            'openai_api_key': self.openai_key.text(),
            'chatglm_api_key': self.chatglm_key.text(),
            'target_language': self.target_lang.currentText(),
            'feedback_language': self.feedback_lang.currentText(),
            'temperature': float(self.temperature.text() or 0.7),
            'max_retries': int(self.max_retries.text() or 3),
            'retry_delay': int(self.retry_delay.text() or 1),
            'timeout': int(self.timeout.text() or 60)
        }
        
        if updates['api_provider'] == 'OpenAI':
            updates['openai_model'] = self.model_combo.currentText()
        else:
            updates['chatglm_model'] = self.model_combo.currentText()
            
        return updates

    def save_config(self):
        """Save configuration changes"""
        try:
            updates = self.get_config_updates()
            self.config_manager.save_config(updates)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save configuration: {str(e)}")

    def test_connection(self):
        """Test API connection"""
        try:
            updates = self.get_config_updates()
            self.config_manager.save_config(updates)
            
            result = self.api_handler.generate_examples("test", count=1)
            QMessageBox.information(self, "Success", "API connection test successful!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Connection test failed: {str(e)}")

    def is_night_mode(self) -> bool:
        """Check if Anki is in night mode"""
        from aqt import mw
        return mw.pm.night_mode()
