from app.core.config import settings

print("Testing Gyani AI Configuration...")
print(f"App Name: {settings.APP_NAME}")
print(f"Debug Mode: {settings.DEBUG}")
print(f"Default Model: {settings.DEFAULT_MODEL}")
print(f"Model API Keys Mapping: {settings.MODEL_API_KEYS}")
print(f"API Key for Llama: {settings.get_api_key_for_model('meta-llama/llama-3.1-405b-instruct')}")
print("Configuration test passed! ✅")