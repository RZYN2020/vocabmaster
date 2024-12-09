import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class APIConfig:
    """API configuration settings"""
    provider: str
    openai_api_key: str
    chatglm_api_key: str
    openai_model: str
    chatglm_model: str
    temperature: float
    max_retries: int
    retry_delay: int
    timeout: int

@dataclass
class LanguageConfig:
    """Language configuration settings"""
    target_language: str
    feedback_language: str

class ConfigManager:
    """Manages configuration settings for the VocabMaster addon"""
    
    DEFAULT_CONFIG = {
        'api_provider': 'OpenAI',
        'openai_api_key': '',
        'chatglm_api_key': '',
        'target_language': 'English',
        'feedback_language': 'English',
        'openai_model': 'gpt-3.5-turbo',
        'chatglm_model': 'glm-4',
        'temperature': 0.7,
        'max_retries': 3,
        'retry_delay': 1,
        'timeout': 60
    }

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    self._validate_config(config)
                    return config
            return self.DEFAULT_CONFIG.copy()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading config: {e}")

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration values"""
        required_fields = {
            'api_provider': str,
            'temperature': (int, float),
            'max_retries': int,
            'retry_delay': (int, float),
            'timeout': int
        }

        for field, expected_type in required_fields.items():
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(config[field], expected_type):
                raise ValueError(f"Invalid type for {field}")

        if config['api_provider'] not in ['OpenAI', 'ChatGLM']:
            raise ValueError("Invalid API provider")

        if config['api_provider'] == 'OpenAI' and not config['openai_api_key']:
            raise ValueError("OpenAI API key is required")
        elif config['api_provider'] == 'ChatGLM' and not config['chatglm_api_key']:
            raise ValueError("ChatGLM API key is required")

    def save_config(self, updates: Dict[str, Any]) -> None:
        """Save updated configuration"""
        new_config = self._config.copy()
        new_config.update(updates)
        self._validate_config(new_config)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=4)
        
        self._config = new_config

    @property
    def api_config(self) -> APIConfig:
        """Get API configuration"""
        return APIConfig(
            provider=self._config['api_provider'],
            openai_api_key=self._config['openai_api_key'],
            chatglm_api_key=self._config['chatglm_api_key'],
            openai_model=self._config['openai_model'],
            chatglm_model=self._config['chatglm_model'],
            temperature=self._config['temperature'],
            max_retries=self._config['max_retries'],
            retry_delay=self._config['retry_delay'],
            timeout=self._config['timeout']
        )

    @property
    def language_config(self) -> LanguageConfig:
        """Get language configuration"""
        return LanguageConfig(
            target_language=self._config['target_language'],
            feedback_language=self._config['feedback_language']
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        updates = {key: value}
        self.save_config(updates)
