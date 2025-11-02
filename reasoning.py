import json
import re

class Reasoner:
    def __init__(self, kb_path="kb.json"):
        with open(kb_path, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

        # Handle both list and dict structures
        if isinstance(self.kb, list):
            self.intents = self.kb
        elif isinstance(self.kb, dict) and "intents" in self.kb:
            self.intents = self.kb["intents"]
        else:
            self.intents = []

    def preprocess(self, text):
        """Clean and normalize user input"""
        return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower()).strip()

    def match_intent(self, user_input):
        user_input = self.preprocess(user_input)

        best_match = None
        best_score = 0

        # Simple word-level matching
        for intent in self.intents:
            for example in intent.get("examples", []):
                example_clean = self.preprocess(example)
                words = example_clean.split()

                match_count = sum(1 for w in words if w in user_input.split())
                score = match_count / max(len(words), 1)

                if score > best_score:
                    best_score = score
                    best_match = intent

        if best_match and best_score > 0.4:  # 40% match confidence
            return best_match.get("response", "Okay.")
        return "I’m not sure I understand 🤔. Could you rephrase that?"

    def reason(self, user_input):
        return self.match_intent(user_input)
