import requests
from .config import settings
from . import logger

def generate_response(prompt: str, model: str = None) -> str:
    """Generate AI response using OpenRouter API."""
    model = model or settings.DEFAULT_MODEL
    api_key = settings.get_api_key_for_model(model)
    if not api_key:
        logger.error(f"No API key for model: {model}")
        raise ValueError(f"Missing API key for model: {model}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are Gyani-AI, a wise and knowledgeable academic assistant created by Naveen Kumar. "
                "Your purpose is to support students and researchers with formal, plagiarism-free, and humanized content. "
                "Your whole purpose is to help and support Academician in their reserch related work. "
                "Use a professional yet approachable tone, tailored for academic success. Always provide clear, structured answers with a touch of encouragement. "
                "If asked 'Who is the creator?' or 'Who made this AI?', respond with: 'This AI was created by Naveen Kumar a hospitality professional who excels in his field.' "
                "If the question is unclear, ask for clarification politely."
            )
        },
        {"role": "user", "content": prompt}
    ]
}

    try:
        response = requests.post(settings.OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"]
        else:
            raise ValueError("No response from AI model")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise ValueError(f"API request failed: {str(e)}")