import re

try:
    import spacy
    nlp_spacy = spacy.load("en_core_web_sm")
except Exception:
    nlp_spacy = None

def simple_intent_entity(text: str):
    t = text.lower()
    entities = []
    intent = "unknown"

    if re.search(r"\b(account|login|log in|sign in)\b", t):
        intent = "account_access"
        if re.search(r"\b(lock|locked|blocked)\b", t):
            entities.append("locked")
        if re.search(r"\b(password|passcode)\b", t):
            entities.append("password")
    elif re.search(r"\b(email|mail)\b", t):
        intent = "service_status"
        entities.append("email")
    elif re.search(r"\b(network|internet|wifi)\b", t):
        intent = "network_issue"
    elif re.search(r"\b(help|support|how to)\b", t):
        intent = "help_request"
    elif re.search(r"\b(why|explain|reason)\b", t):
        intent = "explain_request"

    if re.fullmatch(r"\s*(yes|yep|yeah|no|nah|nope)\s*", t):
        intent = "yes_no"

    return {"intent": intent, "entities": entities, "text": text}

def spacy_intent_entity(text: str):
    if not nlp_spacy:
        return simple_intent_entity(text)
    doc = nlp_spacy(text)
    ents = [ent.text for ent in doc.ents]
    if any(tok.lemma_.lower() in ("lock","locked","block") for tok in doc):
        intent = "account_access"
    elif any(tok.lemma_.lower() in ("network","internet","wifi") for tok in doc):
        intent = "network_issue"
    else:
        intent = "unknown"
    return {"intent": intent, "entities": ents, "text": text}

def parse(text, use_spacy=False):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    tokens = text.split()
    return {
        "original": text,
        "tokens": tokens
    }
