keywords = ["Позначити_точку", "Побудувати_відрізок",
            "Побудувати_перпендикуляр", "до"]

# Define basic forms of keywords to match different inflected forms
keyword_bases = {
    "Позначити_точк": "Позначити_точку",
    "Побудувати_відріз": "Побудувати_відрізок",
    "Побудувати_перпендикуляр": "Побудувати_перпендикуляр",
    "до": "до"
}


def normalize_keyword(word):
    """ Normalize a keyword to its base form if applicable. """
    for base in keyword_bases:
        if word.startswith(base):
            return keyword_bases[base]
    return word


def lexer_analyzer(code):
    tokens = []
    current_token = ""

    for char in code:
        if char.isalpha() or char == '_':
            current_token += char
        elif char.isspace():
            if current_token:
                tokens.append(get_token_type(current_token))
                current_token = ""
        elif char in ";#":
            if current_token:
                tokens.append(get_token_type(current_token))
                current_token = ""
            tokens.append(("DELIMITER", char))
        else:
            if current_token:
                tokens.append(get_token_type(current_token))
                current_token = ""
            print(f"Error: Invalid character '{char}'")

    if current_token:
        tokens.append(get_token_type(current_token))

    return tokens


def get_token_type(token):
    normalized_token = normalize_keyword(token)
    if normalized_token in keywords:
        return ("KEYWORD", normalized_token)
    elif token.isidentifier():
        return ("IDENTIFIER", token)
    else:
        print(f"Error: Invalid identifier: {token}")
        return ("ERROR", token)
