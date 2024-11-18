from lexer import lexer_analyzer
from parser import Parser
from semantic_analyzer import semantic_analysis
import matplotlib.pyplot as plt
from graphics import draw_line, draw_perpendicular

code = "ПОЗНАЧИТИ_ТОЧКf A1; Побудувати_відрізок BM1; Побудувати_перпендикуляр MN до BM1; ПОЗНАЧИТИ_ТОЧКf A; Побудувати_відрізок CJ; Відрізок K1L перетинає відрізок CJ;#"

try:
    tokens = lexer_analyzer(code)
    print("Lexer output:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    parsed_tree = parser.parse()
    print("\nParser output (Syntax Tree):")
    print(parsed_tree)

    commands = semantic_analysis(parsed_tree)
    print("\nSemantic analyzer output:")
    for cmd in commands:
        print(cmd)

    plt.figure(figsize=(10, 6))
    for cmd in commands:
        try:
            exec(cmd)
        except Exception as e:
            print(f"Error executing command '{cmd}': {str(e)}")

    plt.axis('equal')
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1))
    plt.grid(True)
    plt.title("Geometric Construction")
    plt.savefig('geometric_construction.png')
    print("\nPlot saved as 'geometric_construction.png'")
    print("Execution completed. Check the generated plot image.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
