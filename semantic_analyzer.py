def semantic_analysis(parsed_tree):
    commands = []
    points = {}

    def process_node(node):
        if node.value.startswith("Sentence (Позначити_точку)"):
            point_name = node.children[0].value.split(': ')[1]
            if point_name not in points:
                x, y = len(points) * 2, 0
                points[point_name] = (x, y)
                commands.append(f"plt.scatter({x}, {y}, label='{point_name}')")
                commands.append(
                    f"plt.text({x}, {y}, '{point_name}', fontsize=12, ha='right')")
            else:
                print(f"Point {point_name} already exists. Skipping.")

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
                else:
                    print(f"Point {p} in 'відрізок' already exists. Skipping.")
            commands.append(f"draw_line({points[p1]}, {
                            points[p2]}, color='blue')")

        elif node.value.startswith("Sentence (Побудувати_перпендикуляр)"):
            perp_points = node.children[0].value.split(': ')[1]
            line = node.children[2].value.split(': ')[1]

            if len(line) == 2 and len(perp_points) == 2:
                base_p1, base_p2 = line[0], line[1]
                perp_start, perp_end = perp_points[0], perp_points[1]

                # Verify base line points exist
                if base_p1 not in points or base_p2 not in points:
                    raise ValueError(f"Line points {base_p1} or {
                                     base_p2} not defined")

                # Calculate midpoint of base line
                base_midpoint_x = (points[base_p1][0] + points[base_p2][0]) / 2
                # Assuming horizontal line
                base_midpoint_y = points[base_p1][1]

                # If the perpendicular end point exists on the base line, swap points
                if perp_end in [base_p1, base_p2]:
                    perp_start, perp_end = perp_end, perp_start

                # Create or use perpendicular start point
                if perp_start in [base_p1, base_p2]:
                    # If start point is on base line, use its existing position
                    start_x, start_y = points[perp_start]
                else:
                    # Otherwise, place it at midpoint
                    start_x, start_y = base_midpoint_x, base_midpoint_y
                    if perp_start not in points:
                        points[perp_start] = (start_x, start_y)
                        commands.append(
                            f"plt.scatter({start_x}, {start_y}, label='{perp_start}')")
                        commands.append(
                            f"plt.text({start_x}, {start_y}, '{perp_start}', fontsize=12, ha='right')")
                    else:
                        print(
                            f"Point {perp_start} in 'перпендикуляр' already exists. Skipping.")
                # Calculate base line length for perpendicular height
                base_length = ((points[base_p2][0] - points[base_p1][0])**2 +
                               (points[base_p2][1] - points[base_p1][1])**2)**0.5
                height = base_length / 2

                # Create end point if it doesn't exist
                if perp_end not in points:
                    end_x = start_x
                    end_y = start_y + height
                    points[perp_end] = (end_x, end_y)
                    commands.append(
                        f"plt.scatter({end_x}, {end_y}, label='{perp_end}')")
                    commands.append(
                        f"plt.text({end_x}, {end_y}, '{perp_end}', fontsize=12, ha='right')")
                else:
                    print(
                        f"Point {perp_end} in 'перпендикуляр' already exists. Skipping.")
                # Draw the perpendicular line
                commands.append(f"draw_line({points[perp_start]}, {
                                points[perp_end]}, color='red')")

        for child in node.children:
            process_node(child)

    process_node(parsed_tree)
    return commands
