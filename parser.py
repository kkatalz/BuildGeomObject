from lexer import lexer_analyzer

# <текст> ::= <список речень> #
# <список речень> ::= <речення> <продовження списку>
# <продовження списку> ::= ; <список речень> | <пусто>
# <речення> ::= <простий оператор>
# <простий оператор> ::= "Позначити_точку" <точка> |
#                        "Побудувати_відрізок" <пара імен> |
#                        "Побудувати_перпендикуляр <перпендикуляр> до <відрізок>
# <пара імен> ::= <точка> <точка>
# <точка> ::= anyLetter
# <пусто> ::=
# <відрізок> :: = <пара імен>
# <перпендикуляр> ::= <пара імен> до <відрізок>  (відрізок одна точка якого знаходиться на відрізку)


#  "Побудувати_перпендикуляр <пара імен> до відрізок. визначити відрізок перпендикуляр


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def parse(self):
        return self.parse_text()

    def parse_text(self):
        root = TreeNode("Text")
        sentences = self.parse_sentences()
        root.add_child(sentences)
        if self.current_token < len(self.tokens) and self.tokens[self.current_token][1] == '#':
            root.add_child(TreeNode("EndMarker: #"))
            self.current_token += 1
        else:
            raise SyntaxError("Expected end of input (#) after statements")
        return root

    def parse_sentences(self):
        sentences_node = TreeNode("Sentences")
        while self.current_token < len(self.tokens) and self.tokens[self.current_token][1] != '#':
            sentence = self.parse_sentence()
            sentences_node.add_child(sentence)
            if self.current_token < len(self.tokens) and self.tokens[self.current_token][1] == ';':
                sentences_node.add_child(TreeNode("Delimiter: ;"))
                self.current_token += 1
            else:
                print("\n Missed ' ; ' after ",
                      self.tokens[self.current_token-1])
                raise SyntaxError(
                    "Expected end of the sentence (;) in sentences")

        return sentences_node

    def parse_sentence(self):
        if self.current_token >= len(self.tokens):
            raise SyntaxError("No more tokens to parse")

        token = self.tokens[self.current_token]
        if token[0] == 'KEYWORD':
            sentence_node = TreeNode(f"Sentence ({token[1]})")
            self.current_token += 1

            if token[1] == "Позначити_точку":
                sentence_node.add_child(self.parse_identifier())
            elif token[1] == "Побудувати_відрізок":
                sentence_node.add_child(self.parse_identifier_pair())
            elif token[1] == "Побудувати_перпендикуляр":
                sentence_node.add_child(self.parse_identifier())
                if self.tokens[self.current_token][1] == 'до':
                    sentence_node.add_child(TreeNode("Keyword: до"))
                    self.current_token += 1
                else:
                    raise SyntaxError(
                        "Expected 'до' in 'Побудувати_перпендикуляр'")
                sentence_node.add_child(self.parse_identifier())
            else:
                raise SyntaxError(f"Unknown keyword: {token[1]}")

            return sentence_node
        else:
            raise SyntaxError(
                f"Invalid sentence structure: Unexpected token {token}")

    def parse_identifier(self):
        if self.current_token < len(self.tokens) and self.tokens[self.current_token][0] == 'IDENTIFIER':
            identifier = TreeNode(
                f"Identifier: {self.tokens[self.current_token][1]}")
            self.current_token += 1
            return identifier
        else:
            raise SyntaxError("Expected identifier")

    def parse_identifier_pair(self):
        if self.current_token < len(self.tokens) and self.tokens[self.current_token][0] == 'IDENTIFIER':
            points = self.tokens[self.current_token][1]
            if len(points) == 2:
                pair_node = TreeNode("IdentifierPair")
                pair_node.add_child(TreeNode(f"Identifier: {points[0]}"))
                pair_node.add_child(TreeNode(f"Identifier: {points[1]}"))
                self.current_token += 1
                return pair_node
            else:
                raise SyntaxError(
                    "Expected two-letter identifier for 'Побудувати_відрізок'")
        else:
            raise SyntaxError("Expected identifier pair")
