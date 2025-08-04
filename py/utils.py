def extract_outermost_braces(text):
    """Extract from first { to last }"""
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and start < end:
        return text[start:end+1]
    return None