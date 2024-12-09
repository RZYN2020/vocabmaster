from ast import Return
import os
import json
import re
import requests
import time
from typing import List, Dict, Optional, Union
from datetime import datetime
import jwt
import uuid

class RateLimitError(Exception):
    """Exception raised when API rate limit is exceeded"""
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after

class APIError(Exception):
    """Base exception for API related errors"""
    pass

class ConfigError(Exception):
    """Exception raised for configuration related errors"""
    pass

from typing import Dict, List

class MessagePreparer:
    def __init__(self, config: Dict):
        self.config = config

    def _prepare_messages(self, action: str, params: Dict) -> List[Dict[str, str]]:
        """Prepare messages for API request based on action with optimized prompts."""
        action_handlers = {
            "test": self._handle_test,
            "generate_article": self._handle_generate_article,
            "evaluate_sentence": self._handle_evaluate_sentence,
            "generate_examples": self._handle_generate_examples,
        }

        handler = action_handlers.get(action)
        if not handler:
            raise ValueError(f"Unknown action: {action}")

        return [{"role": "user", "content": handler(params)}]

    def _handle_test(self, params: Dict) -> str:
        return f"Test message received: \"{params['message']}\"."

    def _handle_generate_article(self, params: Dict) -> str:
        words = ', '.join(params['words'])
        """Generate an article using the selected words"""
        target_lang = self.config['target_language']
        prompt = f"""Please write a short article (150-200 words) in {target_lang} that naturally incorporates these vocabulary words: {', '.join(words)}.
        Make sure to use each word in a clear context that demonstrates its meaning.
        Format the article with proper paragraphs and highlight each vocabulary word in bold."""
        return prompt

    def _handle_evaluate_sentence(self, params: Dict) -> str:
        target_lang = self.config['target_language']
        feedback_lang = self.config['feedback_language']
        prompt = f"""Please evaluate this {target_lang} sentence using the word '{params['target_word']}':
        "{params['sentence']}"
        
        Provide feedback in {feedback_lang} on:
        1. Grammar and natural usage
        2. Whether the word is used correctly
        3. Suggestions for improvement if needed"""
        return prompt

    def _handle_generate_examples(self, params: Dict) -> str:
        count = params.get('count', 3)
        target_lang = self.config['target_language']
        prompt = f"""Please generate {count} example sentences in {target_lang} using the word '{params['word']}'.
        Remember the reponse should only contain sentences and not any other text.
        Make the sentences:
        1. Natural and contextual
        2. Varied in structure
        3. Clear in demonstrating the word's meaning"""
        return prompt
    
class APIHandler:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.default_config = {
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
            'timeout': 60,
            'chatglm_endpoint': 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
        }
        self.config = self.load_config()
        self.preparer = MessagePreparer(self.config)
        self.setup_api()

    def load_config(self) -> Dict:
        """Load configuration from file with validation"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    config = self.default_config.copy()
                    config.update(loaded_config)
                    self._validate_config(config)
                    return config
            return self.default_config.copy()
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ConfigError(f"Error loading config: {e}")

    def _validate_config(self, config: Dict) -> None:
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
                raise ConfigError(f"Missing required field: {field}")
            if not isinstance(config[field], expected_type):
                raise ConfigError(f"Invalid type for {field}: expected {expected_type}, got {type(config[field])}")

        if config['api_provider'] not in ['OpenAI', 'ChatGLM']:
            raise ConfigError("Invalid API provider. Must be 'OpenAI' or 'ChatGLM'")

        if config['api_provider'] == 'OpenAI' and not config['openai_api_key']:
            raise ConfigError("OpenAI API key is required when using OpenAI provider")
        elif config['api_provider'] == 'ChatGLM' and not config['chatglm_api_key']:
            raise ConfigError("ChatGLM API key is required when using ChatGLM provider")

    def setup_api(self) -> None:
        """Set up API client based on provider"""
        if self.config['api_provider'] == 'OpenAI':
            import openai
            openai.api_key = self.config['openai_api_key']
        # Add setup for other providers as needed

    def save_config(self, config_updates: Dict) -> None:
        """Save updated configuration"""
        try:
            new_config = self.config.copy()
            new_config.update(config_updates)
            self._validate_config(new_config)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4)
            
            self.config = new_config
            self.setup_api()
        except Exception as e:
            raise ConfigError(f"Error saving config: {e}")

    def _make_api_request(self, action: str, params: Dict) -> str:
        """Make API request with retry logic"""
        retries = 0
        while retries < self.config['max_retries']:
            try:
                if self.config['api_provider'] == 'OpenAI':
                    return self._make_openai_request(action, params)
                elif self.config['api_provider'] == 'ChatGLM':
                    return self._make_chatglm_request(action, params)
                else:
                    raise APIError(f"Unsupported API provider: {self.config['api_provider']}")
            except RateLimitError:
                raise
            except Exception as e:
                retries += 1
                if retries == self.config['max_retries']:
                    raise APIError(f"API request failed after {retries} retries: {e}")
                time.sleep(self.config['retry_delay'])

    def _make_openai_request(self, action: str, params: Dict) -> str:
        """Make request to OpenAI API"""
        import openai
        try:
            messages = self._prepare_messages(action, params)
            response = openai.ChatCompletion.create(
                model=self.config['openai_model'],
                messages=messages,
                temperature=self.config['temperature']
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError as e:
            raise RateLimitError(str(e), retry_after=60)
        except Exception as e:
            raise APIError(f"OpenAI API error: {e}")

    def _make_chatglm_request(self, action: str, params: Dict) -> str:
        """Make request to ChatGLM API"""
        try:
            api_key = self.config['chatglm_api_key']
            print(f"[DEBUG] Using API Key: {api_key[:10]}...")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            messages = self._prepare_messages(action, params)
            data = {
                "model": "chatglm_std",
                "messages": messages,  # Send all messages
                "temperature": self.config['temperature'],
                "stream": False,  # Explicitly set stream to false
                "request_id": str(uuid.uuid4())
            }
            print(f"[DEBUG] Request Data: {data}")
            
            endpoint = "https://open.bigmodel.cn/api/paas/v4/chat/completions"  # Use v4 chat completions endpoint
            print(f"[DEBUG] Using endpoint: {endpoint}")
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                timeout=self.config['timeout']
            )
            
            print(f"[DEBUG] Response Status: {response.status_code}")
            print(f"[DEBUG] Response Content: {response.text}")
            
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise RateLimitError("ChatGLM rate limit exceeded", retry_after=retry_after)
            elif response.status_code != 200:
                print(f"[DEBUG] Response Headers: {dict(response.headers)}")
                raise APIError(f"ChatGLM API error: HTTP {response.status_code}\n{response.text}")
            
            try:
                response_data = response.json()
                if not response_data.get('choices'):
                    raise APIError(f"Invalid response format from ChatGLM API: {response_data}")
                    
                return response_data['choices'][0]['message']['content'].strip()
                
            except json.JSONDecodeError as e:
                raise APIError(f"Failed to parse ChatGLM API response: {e}")
                
        except requests.exceptions.RequestException as e:
            raise APIError(f"ChatGLM API error: {e}")

    def _prepare_messages(self, action: str, params: Dict) -> List[Dict[str, str]]:
        """Prepare messages for API request based on action"""
        return self.preparer._prepare_messages(action, params)

    def test_connection(self) -> bool:
        """Test API connection by making a simple request"""
        try:
            test_message = "Hello! This is a test message to verify the API connection."
            messages = [{"role": "user", "content": test_message}]
            
            if self.config['api_provider'] == 'ChatGLM':
                return self._make_chatglm_request("test", {"message": test_message}) is not None
            elif self.config['api_provider'] == 'OpenAI':
                return self._make_openai_request("test", {"message": test_message}) is not None
            else:
                raise APIError(f"Unsupported API provider: {self.config['api_provider']}")
        except Exception as e:
            raise APIError(f"Connection test failed: {str(e)}")

    def generate_article(self, words: List[str]) -> str:
        """Generate an article using given words"""
        return self._make_api_request("generate_article", {"words": words})

    def evaluate_sentence(self, sentence: str, target_word: str) -> str:
        """Evaluate a sentence using target word"""
        return self._make_api_request("evaluate_sentence", {
            "sentence": sentence,
            "target_word": target_word
        })

    def generate_examples(self, word: str, count: int = 3) -> str:
        """Generate example sentences using word"""
        return self._make_api_request("generate_examples", {
            "word": word,
            "count": count
        })
