from lexer import lexer_analyzer
from parser import Parser
from semantic_analyzer import semantic_analysis
import matplotlib.pyplot as plt
from graphics import draw_line, draw_perpendicular

code = "ПОЗНАЧИТИ_ТОЧКf A1 (0, 4); ПОЗНАЧИТИ_ТОЧКf B1 (0, 4); Побудувати_відрізок B1M1; Побудувати_перпендикуляр N1M1 до B1M1; ПОЗНАЧИТИ_ТОЧКf A; Побудувати_відрізок C1J1; Відрізок K1L перетинає відрізок C1J1;#"

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
