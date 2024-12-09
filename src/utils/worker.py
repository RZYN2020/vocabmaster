from PyQt6.QtCore import QThread, pyqtSignal
from ..api.api_handler import APIHandler, RateLimitError, APIError

class AIWorker(QThread):
    """Worker thread for handling AI API requests"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    rate_limit = pyqtSignal(str, int)
    result_ready = pyqtSignal(str)  # Signal for streaming results

    def __init__(self, action: str, params: dict, config_path: str):
        super().__init__()
        self.action = action
        self.params = params
        self.config_path = config_path
        self.api_handler = None
        self._is_running = True

    def run(self):
        """Execute the API request in a separate thread"""
        try:
            self.api_handler = APIHandler(self.config_path)
            
            if not self._is_running:
                return
                
            result = None
            if self.action == "generate_article":
                result =self.api_handler.generate_article(self.params["words"])
            elif self.action == "evaluate_sentence":
                result = self.api_handler.evaluate_sentence(
                    self.params["sentence"],
                    self.params["target_word"]
                )
            elif self.action == "generate_examples":
                result = self.api_handler.generate_examples(
                    self.params["word"],
                    self.params.get("count", 3)
                )
            else:
                raise ValueError(f"Unknown action: {self.action}")
                
            if self._is_running and result is not None:
                self.finished.emit(result)
                
        except Exception as e:
            if not self._is_running:
                return
                
            if isinstance(e, RateLimitError):
                self.rate_limit.emit(str(e), e.retry_after)
            elif isinstance(e, APIError):
                self.error.emit(f"API Error: {str(e)}")
            else:
                self.error.emit(f"Error: {str(e)}")
                
    def stop(self):
        """Stop the worker thread"""
        self._is_running = False
