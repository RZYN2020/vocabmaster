import os
import sys
import json

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.api.api_handler import APIHandler

import requests
import time

def setup_test_config(api_provider='ChatGLM'):
    """Setup test configuration"""
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_config_path = os.path.join(addon_dir, "config.json")
    test_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    
    # Load main config if available
    if os.path.exists(main_config_path):
        with open(main_config_path, 'r') as f:
            main_config = json.load(f)
    else:
        raise ValueError("Main config file not found")
    
    # Create test config
    config = {
        'api_provider': api_provider,
        'temperature': 0.7,
        'max_retries': 3,
        'retry_delay': 1,
        'timeout': 60
    }
    
    # Copy API keys from main config
    if api_provider == 'ChatGLM':
        config['chatglm_model'] = 'glm-4'
        config['chatglm_api_key'] = main_config.get('chatglm_api_key', '')
        if not config['chatglm_api_key']:
            raise ValueError("ChatGLM API key not found in config")
    else:
        config['openai_model'] = 'gpt-3.5-turbo'
        config['openai_api_key'] = main_config.get('openai_api_key', '')
        if not config['openai_api_key']:
            raise ValueError("OpenAI API key not found in config")
    
    # Save test config
    with open(test_config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    return test_config_path

def test_api_connection(api_provider='ChatGLM'):
    """Test API connection and functionality"""
    print(f"\nTesting {api_provider} API Integration")
    print("=" * 50)
    
    # Setup test configuration
    config_path = setup_test_config(api_provider)
    
    # Initialize API handler
    api = APIHandler(config_path)
    
    try:
        # Test connection
        print("\n[1] Testing API Connection...")
        api.test_connection()
        print("[+] Connection test successful!")
        
        # Test article generation
        print("\n[2] Testing Article Generation...")
        words = ["ephemeral", "ubiquitous", "serendipity"]
        article = api.generate_article(words)
        print("Generated Article:")
        print(article)
        print("[+] Article generation successful!")
        
        # Test sentence evaluation
        print("\n[3] Testing Sentence Evaluation...")
        sentence = "The ephemeral nature of social media trends makes them fascinating to study."
        word = "ephemeral"
        evaluation = api.evaluate_sentence(sentence, word)
        print("Sentence Evaluation:")
        print(evaluation)
        print("[+] Sentence evaluation successful!")
        
        # Test example generation
        print("\n[4] Testing Example Generation...")
        examples = api.generate_examples(word)
        print("Generated Examples:")
        print(examples)
        print("[+] Example generation successful!")
        
        print("\n[+] All tests passed successfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Network Error: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[-] Invalid API Response: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error: {str(e)}")
        sys.exit(1)

def test_all_providers():
    """Test all supported API providers"""
    providers = ['ChatGLM', 'OpenAI']
    for provider in providers:
        try:
            test_api_connection(provider)
        except Exception as e:
            print(f"[-] {provider} tests failed: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['ChatGLM', 'OpenAI']:
        test_api_connection(sys.argv[1])
    else:
        test_all_providers()
