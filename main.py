from lexer import lexer_analyzer
from parser import Parser
from semantic_analyzer import semantic_analysis
import matplotlib.pyplot as plt
from graphics import draw_line, draw_perpendicular

code = "ПОЗНАЧИТИ_ТОЧКf A1 (3, 4); ПОЗНАЧИТИ_ТОЧКf B1 (0, 4); Побудувати_відрізок BM1; Побудувати_перпендикуляр N1M1 до BM1; ПОЗНАЧИТИ_ТОЧКf A; Побудувати_відрізок C1J1; Відрізок K1L перетинає відрізок C1J1;#"


try:
    with open('grammar.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        print("---" * 20)
        print("Contents of grammar.txt:\n")
        print(content)
        print("---" * 20)

except FileNotFoundError:
    print("Error: The file 'grammar.txt' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print("---" * 20)
print("\nTask to implement: \n", code)
print("---" * 20)

try:
    tokens = lexer_analyzer(code)
    print("\n LEXER OUTPUT:")
    for token in tokens:
        print()
        print(token)
    print("---" * 20)

    parser = Parser(tokens)
    parsed_tree = parser.parse()
    print("\n PARSER OUTPUT (SYNTAX TREE):")
    print(parsed_tree)
    print("---" * 20)

    commands = semantic_analysis(parsed_tree)
    print("\n SEMANTIC ANALYZER OUTPUT:")
    for cmd in commands:
        print(cmd)
    print("---" * 20)

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
