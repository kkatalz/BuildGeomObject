def semantic_analysis(parsed_tree):
    commands = []
    points = {}

    def process_node(node):
        if node.value.startswith("Sentence (Позначити_точку)"):
            point_name = node.children[0].value.split(': ')[1]
            x, y = len(points) * 2, 0
            points[point_name] = (x, y)
            commands.append(f"plt.scatter({x}, {y}, label='{point_name}')")
            commands.append(
                f"plt.text({x}, {y}, '{point_name}', fontsize=12, ha='right')")

        elif node.value.startswith("Sentence (Побудувати_відрізок)"):
            p1 = node.children[0].children[0].value.split(': ')[1]
            p2 = node.children[0].children[1].value.split(': ')[1]
            for p in [p1, p2]:
                if p not in points:
                    x, y = len(points) * 2, 0
                    points[p] = (x, y)
                    commands.append(f"plt.scatter({x}, {y}, label='{p}')")
                    commands.append(
                        f"plt.text({x}, {y}, '{p}', fontsize=12, ha='right')")
            commands.append(f"draw_line({points[p1]}, {
                            points[p2]}, color='blue')")

        elif node.value.startswith("Sentence (Побудувати_перпендикуляр)"):
            name = node.children[0].value.split(': ')[1]
            line = node.children[2].value.split(': ')[1]
            if len(line) == 2:
                base_p1, base_p2 = line[0], line[1]
                if base_p1 in points and base_p2 in points:
                    commands.append(f"draw_perpendicular('{
                                    name}', [{points[base_p1]}, {points[base_p2]}], color='red')")
                else:
                    raise ValueError(f"Line points {base_p1} or {
                                     base_p2} not defined")

        for child in node.children:
            process_node(child)

    process_node(parsed_tree)
    return commands
