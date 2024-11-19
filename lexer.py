keywords = ["Позначити_точку", "Побудувати_відрізок",
            "Побудувати_перпендикуляр", "до", "перетинає", "відрізок"]

keyword_bases = {
    "позначити_точк": "Позначити_точку",
    "побудувати_відріз": "Побудувати_відрізок",
    "провести_відріз": "Побудувати_відрізок",
    "побудувати_перпендикуляр": "Побудувати_перпендикуляр",
    "перетинає": "перетинає",
    "відрізок": "відрізок"
}


def normalize_keyword(word):
    word = word.lower()
    for base in keyword_bases:
        if word.startswith(base):
            return keyword_bases[base]
    return word


def lexer_analyzer(code):
    tokens = []
    current_token = ""
    inside_coordinates = False  # Track if we're inside a coordinate block

    for char in code:
        if inside_coordinates:
            if char == ')':  # End of coordinates
                current_token += char
                tokens.append(get_token_type(current_token))
                current_token = ""
                inside_coordinates = False
            else:
                current_token += char  # Continue collecting coordinates
        elif char.isalnum() or char == '_':
            current_token += char
        elif char == '(':
            if current_token:  # Save previous token
                tokens.append(get_token_type(current_token))
                current_token = ""
            current_token += char
            inside_coordinates = True
        elif char.isspace():
            if current_token:
                tokens.append(get_token_type(current_token))
                current_token = ""
        elif char in ";#":
            if current_token:
                tokens.append(get_token_type(current_token))
                current_token = ""
            tokens.append(("DELIMITER", char))
        elif char == ',' and inside_coordinates:  # Allow comma inside coordinates
            current_token += char
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
    elif token.startswith("(") and token.endswith(")"):
        try:
            x, y = map(float, token[1:-1].split(","))
            return ("COORDINATES", (x, y))
        except ValueError:
            print(f"Error: Invalid coordinates format: {token}")
            return ("ERROR", token)
    else:
        print(f"Error: Invalid identifier: {token}")
        return ("ERROR", token)
