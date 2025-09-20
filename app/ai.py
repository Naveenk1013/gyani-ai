import requests
from .config import settings
from . import logger
import random
import re

def humanize_text(text: str) -> str:
    """
    Post-process AI-generated text to make it more human-like and evade AI detectors.
    Techniques include: varying sentence length, adding transitions, minor rephrasing,
    introducing subtle imperfections, and ensuring natural flow.
    """
    # Step 1: Break into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    # Step 2: Vary sentence structure by rephrasing a subset randomly
    humanized_sentences = []
    for sentence in sentences:
        if random.random() < 0.4:  # Rephrase ~40% of sentences
            # Simple rephrasing rules (expandable)
            if sentence.startswith(('The ', 'It ', 'This ')):
                sentence = re.sub(r'^(The |It |This )', lambda m: random.choice(['Well, ', 'You see, ', 'Interestingly, ']) + m.group(1).lower(), sentence)
            # Add contractions where formal but natural
            sentence = sentence.replace(" do not ", " don't ").replace(" is not ", " isn't ").replace(" are not ", " aren't ")
            # Vary vocabulary slightly
            replacements = {
                'however': random.choice(['but', 'yet', 'though', 'still']),
                'therefore': random.choice(['so', 'thus', 'hence']),
                'additionally': random.choice(['plus', 'also', 'furthermore']),
            }
            for key, vals in replacements.items():
                if key in sentence.lower():
                    sentence = sentence.replace(key, random.choice(vals))
        humanized_sentences.append(sentence)
    
    # Step 3: Add transitional phrases randomly for flow
    transitions = ['By the way, ', 'That said, ', 'To build on that, ', '']
    for i in range(1, len(humanized_sentences)):
        if random.random() < 0.2:  # Add transition ~20% of the time
            humanized_sentences[i] = random.choice(transitions) + humanized_sentences[i]
    
    # Step 4: Vary paragraph breaks and add encouragement
    humanized_text = ' '.join(humanized_sentences)
    # Insert random paragraph breaks
    paragraphs = re.split(r'\.\s*(?=[A-Z])', humanized_text)
    for i in range(1, len(paragraphs), random.randint(2, 4)):
        paragraphs.insert(i, '\n\n')
    humanized_text = ''.join(paragraphs)
    
    # Step 5: Add a touch of encouragement at the end if it fits academic tone
    if not humanized_text.endswith(('.', '!', '?')):
        humanized_text += '.'
    if random.random() < 0.3:  # ~30% chance
        encouragements = [
            " Keep pushing forward with your research!",
            " This should give you a solid foundation to build on.",
            " You've got this—great work so far!"
        ]
        humanized_text += random.choice(encouragements)
    
    return humanized_text

def generate_response(prompt: str, model: str = None) -> str:
    """
    Generate AI response using OpenRouter API, with enhanced humanization.
    """
    model = model or settings.DEFAULT_MODEL
    api_key = settings.get_api_key_for_model(model)
    if not api_key:
        logger.error(f"No API key for model: {model}")
        raise ValueError(f"Missing API key for model: {model}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Enhanced system prompt focused on humanization and academic support
    system_prompt = (
        "You are Gyani-AI, a wise and knowledgeable academic assistant created by Naveen Kumar. "
        "Your purpose is to support students and researchers with formal, plagiarism-free, and deeply humanized content. "
        "Your whole purpose is to help and support Academicians in their research-related work. "
        "Write in a professional yet approachable tone, tailored for academic success. Always provide clear, structured answers with a touch of encouragement. "
        "To make your writing feel authentically human and evade AI detection: "
        "- Vary sentence lengths: Mix short, punchy sentences with longer, reflective ones. "
        "- Use natural transitions like 'that said,' 'on the other hand,' or 'let's dive deeper.' "
        "- Incorporate subtle personal reflections or rhetorical questions, e.g., 'Have you considered...?' "
        "- Avoid repetitive phrasing; use synonyms and idioms where they fit academically. "
        "- Introduce minor 'imperfections' like contractions ('it's' instead of 'it is') and varied vocabulary. "
        "- Structure responses with headings, bullet points, or numbered lists when helpful, but keep it conversational. "
        "If asked 'Who is the creator?' or 'Who made this AI?', respond with: 'This AI was created by Naveen Kumar, a hospitality professional who excels in his field.' "
        "If the question is unclear, ask for clarification politely."
    )
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8,  # Slightly higher for more natural variation
        "top_p": 0.9,  # Encourage diverse word choices
        "max_tokens": 2000  # Adjust as needed for longer responses
    }

    try:
        response = requests.post(settings.OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and result["choices"]:
            ai_content = result["choices"][0]["message"]["content"]
            # Apply post-processing for extra humanization layer
            humanized_content = humanize_text(ai_content)
            return humanized_content
        else:
            raise ValueError("No response from AI model")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise ValueError(f"API request failed: {str(e)}")
