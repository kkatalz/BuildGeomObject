from lexer import lexer_analyzer
#  файл для реалізації синтаксичного аналізатора.

# <текст> ::= <список речень> #
# <список речень> ::= <речення> <продовження списку>
# <продовження списку> ::= ; <список речень> | <пусто>
# <речення> ::= <простий оператор>
# <простий оператор> ::= "Позначити_точку" <ім’я> |
#                        "Побудувати_відрізок" <ім'я> |
#                        "Побудувати_перпендикуляр <ім’я> до <ім’я>
# <пара імен> ::= <ім’я> <ім’я>
# <ім’я> ::= A | B | C | H


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.parsed_data = []

    def parse(self):
        self.parse_text()
        return self.parsed_data

    def parse_text(self):
        self.parse_sentences()
        if self.current_token < len(self.tokens):
            if self.tokens[self.current_token][1] != '#':
                raise SyntaxError("Expected end of input (#) after statements")
            self.current_token += 1  # Consume the '#'

    def parse_sentences(self):
        while self.current_token < len(self.tokens):
            if self.tokens[self.current_token][1] == '#':
                break  # Stop parsing sentences when we encounter '#'
            self.parse_sentence()
            if self.current_token < len(self.tokens) and self.tokens[self.current_token][1] == ';':
                self.current_token += 1
            else:
                break

    def parse_sentence(self):
        if self.current_token >= len(self.tokens):
            raise SyntaxError("No more tokens to parse")

        token = self.tokens[self.current_token]
        if token[0] == 'KEYWORD':
            statement = {"type": token[1]}
            self.current_token += 1

            if token[1] == "Позначити_точку":
                if self.current_token < len(self.tokens) and self.tokens[self.current_token][0] == 'IDENTIFIER':
                    statement["name"] = self.tokens[self.current_token][1]
                    self.current_token += 1
                else:
                    raise SyntaxError(
                        "Expected identifier for 'Позначити_точку'")

            elif token[1] == "Побудувати_відрізок":
                if self.current_token < len(self.tokens) and self.tokens[self.current_token][0] == 'IDENTIFIER':
                    points = self.tokens[self.current_token][1]
                    if len(points) == 2:  # If it's a single identifier with two letters
                        statement["points"] = [points[0], points[1]]
                    else:
                        raise SyntaxError(
                            "Expected two-letter identifier for 'Побудувати_відрізок'")
                    self.current_token += 1
                else:
                    raise SyntaxError(
                        "Expected identifier for 'Побудувати_відрізок'")

            elif token[1] == "Побудувати_перпендикуляр":
                if self.current_token < len(self.tokens) and self.tokens[self.current_token][0] == 'IDENTIFIER':
                    statement["name"] = self.tokens[self.current_token][1]
                    self.current_token += 1
                else:
                    raise SyntaxError(
                        "Expected an identifier after 'Побудувати_перпендикуляр'")

                if self.current_token < len(self.tokens) and self.tokens[self.current_token][1] == 'до':
                    self.current_token += 1
                else:
                    raise SyntaxError(
                        "Expected 'до' after the identifier in 'Побудувати_перпендикуляр'")

                if self.current_token < len(self.tokens) and self.tokens[self.current_token][0] == 'IDENTIFIER':
                    statement["line"] = self.tokens[self.current_token][1]
                    self.current_token += 1
                else:
                    raise SyntaxError(
                        "Expected an identifier for the line after 'до'")

            self.parsed_data.append(statement)
        else:
            raise SyntaxError(
                f"Invalid sentence structure: Unexpected token {token}")
