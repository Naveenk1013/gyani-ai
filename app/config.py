import os
from pydantic import BaseModel, Field
from typing import Dict
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

class Settings(BaseModel):
    # Get API keys from environment variables ONLY
    LLAMA_API_KEY: str = Field(default=os.getenv('LLAMA_API_KEY', ''))
    QWEEN_CODER_API_KEY: str = Field(default=os.getenv('QWEEN_CODER_API_KEY', ''))
    QWEEN_72B_API_KEY: str = Field(default=os.getenv('QWEEN_72B_API_KEY', ''))
    QWEEN_VL_API_KEY: str = Field(default=os.getenv('QWEEN_VL_API_KEY', ''))

    # OpenRouter API Configuration
    OPENROUTER_API_URL: str = Field(default="https://openrouter.ai/api/v1/chat/completions")

    # Default model to use
    DEFAULT_MODEL: str = Field(default=os.getenv('DEFAULT_MODEL', "meta-llama/llama-3.1-405b-instruct"))

    # App settings
    APP_NAME: str = Field(default="Gyani AI Research Assistant")
    DEBUG: bool = Field(default=os.getenv('DEBUG', 'False').lower() == 'true')

    @property
    def MODEL_API_KEYS(self) -> Dict[str, str]:
        """Return the mapping of models to their API keys"""
        return {
            "meta-llama/llama-3.1-405b-instruct": self.LLAMA_API_KEY,
            "qwen/qwen-2.5-coder-32b-instruct": self.QWEEN_CODER_API_KEY,
            "qwen/qwen-2.5-72b-instruct": self.QWEEN_72B_API_KEY,
            "qwen/qwen2.5-vl-32b-instruct": self.QWEEN_VL_API_KEY
        }

    def get_api_key_for_model(self, model: str) -> str:
        """Get the appropriate API key for the given model"""
        return self.MODEL_API_KEYS.get(model, self.LLAMA_API_KEY)  # Fallback to first key

    def validate_keys(self):
        """Validate that all API keys are set"""
        missing_keys = [key_name for key_name, key_value in self.MODEL_API_KEYS.items() if not key_value]
        if missing_keys:
            raise ValueError(f"Missing API keys for: {', '.join(missing_keys)}")

# Create settings instance
settings = Settings()

# Validate keys on import and raise exception if failed
settings.validate_keys()