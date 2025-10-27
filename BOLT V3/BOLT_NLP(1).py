# Add this after your existing imports
import re

class NLPProcessor:
    def __init__(self):
        self.intent_patterns = {
            'music': ['play', 'music', 'song', 'spotify', 'sound', 'audio', 'tune'],
            'web_search': ['search', 'google', 'find', 'look', 'query'],
            'system': ['system', 'info', 'stats', 'cpu', 'memory', 'performance'],
            'screenshot': ['screenshot', 'capture', 'snap', 'image', 'screen'],
            'open_app': ['open', 'launch', 'start', 'run'],
            'volume': ['volume', 'sound', 'mute', 'unmute', 'loud', 'quiet'],
            'download': ['download', 'get', 'fetch', 'youtube'],
            'terminal': ['terminal', 'cmd', 'command', 'console'],
            'time': ['time', 'date', 'clock', 'when'],
            'greeting': ['hello', 'hi', 'hey', 'greetings']
        }
    
    def extract_intent(self, text):
        tokens = re.findall(r'\w+', text.lower())
        detected_intents = []
        
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in tokens for keyword in keywords):
                detected_intents.append(intent)
        
        return detected_intents[0] if detected_intents else 'unknown'
    
    def nlp_execute_command(self, command):
    """NLP-powered command execution"""
    try:
        # Initialize NLP processor if not exists
        if not hasattr(self, 'nlp_processor'):
            self.nlp_processor = NLPProcessor()
        
        # Extract intent using NLP
        intent = self.nlp_processor.extract_intent(command)
        response = f"NLP detected intent: {intent}"
        
        # Route to appropriate handler based on intent
        if intent == 'music':
            response = self.handle_music(command)
        elif intent == 'web_search':
            response = self.handle_search(command)
        elif intent == 'screenshot':
            response = self.handle_screenshot()
        elif intent == 'open_app':
            response = self.handle_open(command)
        elif intent == 'volume':
            response = self.handle_volume(command)
        elif intent == 'system':
            response = self.handle_system_info()
        elif intent == 'download':
            response = self.handle_download(command)
        elif intent == 'terminal':
            response = self.handle_terminal(command)
        elif intent == 'time':
            response = self.handle_time_date()
        elif intent == 'greeting':
            response = f"Hello {self.user_name}! NLP system recognized your greeting!"
        else:
            # Fallback to original system
            response = f"NLP couldn't classify '{command}'. Trying original system..."
            return self.execute_command_original(command)
        
        # Update UI and speak response
        self.root.after(0, lambda: self.command_complete(response))
        
    except Exception as e:
        error_msg = f"NLP processing error: {str(e)}"
        print(error_msg)
        # Fallback to original system
        self.execute_command_original(command)