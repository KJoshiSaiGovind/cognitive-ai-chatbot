from collections import deque

class DialogueManager:
    def __init__(self, max_history=5):
        self.history = deque(maxlen=max_history)

    def update_history(self, speaker, message):
        self.history.append({"speaker": speaker, "message": message})

    def generate_response(self, parsed_input, reasoned_output):
        return reasoned_output
