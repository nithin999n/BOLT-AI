# Simple NLP test using only built-in Python libraries
import re
import json

def simple_tokenize(text):
    """Basic tokenization"""
    return re.findall(r'\w+', text.lower())

def extract_intent_keywords(text):
    """Extract intent from keywords"""
    tokens = simple_tokenize(text)
    
    # Define intent patterns
    intent_patterns = {
        'music': ['play', 'music', 'song', 'spotify', 'sound'],
        'web_search': ['search', 'google', 'find', 'look'],
        'system': ['system', 'info', 'stats', 'cpu', 'memory'],
        'screenshot': ['screenshot', 'capture', 'snap', 'image'],
        'open': ['open', 'launch', 'start', 'run']
    }
    
    # Find matching intents
    detected_intents = []
    for intent, keywords in intent_patterns.items():
        if any(keyword in tokens for keyword in keywords):
            detected_intents.append(intent)
    
    return detected_intents, tokens

# Test the system
print("Testing Simple NLP Intent Recognition...")

test_commands = [
    "play some music",
    "search for python tutorials", 
    "take a screenshot",
    "open google",
    "show system info"
]

for command in test_commands:
    intents, tokens = extract_intent_keywords(command)
    print(f"Command: '{command}' -> Intents: {intents}")

print("\nSimple NLP system working! Ready to integrate with BOLT AI.")