from lexer import lexer_analyzer
from parser import Parser
from semantic_analyzer import semantic_analysis
import matplotlib.pyplot as plt
import numpy as np
from graphics import draw_line, draw_perpendicular


code = "Позначити_точку A; Побудувати_відрізок BG; Побудувати_перпендикуляр IO до BG;#"
tokens = lexer_analyzer(code)

try:
    tokens = lexer_analyzer(code)
    print("Lexer output:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    parsed_data = parser.parse()
    print("\nParser output:")
    for statement in parsed_data:
        print(statement)

    commands = semantic_analysis(parsed_data)
    print("\nSemantic analyzer output:")
    for cmd in commands:
        print(cmd)

    plt.figure(figsize=(10, 6))
    for cmd in commands:
        exec(cmd)

    plt.axis('equal')
    plt.legend()
    plt.grid(True)
    plt.title("Geometric Construction")
    plt.savefig('geometric_construction.png')
    print("\nPlot saved as 'geometric_construction.png'")
    print("Execution completed. Check the generated plot image.")

except SyntaxError as e:
    print(f"Syntax error caught: {e}")
