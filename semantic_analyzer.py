def semantic_analysis(parsed_data):
    commands = []
    points = {}

    for statement in parsed_data:
        if statement["type"] == "Позначити_точку":
            point_name = statement["name"]
            x, y = len(points) * 2, 0
            points[point_name] = (x, y)
            commands.append(f"plt.scatter({x}, {y}, label='{point_name}')")
            commands.append(
                f"plt.text({x}, {y}, '{point_name}', fontsize=12, ha='right')")

        elif statement["type"] == "Побудувати_відрізок":
            p1, p2 = statement["points"]
            if p1 not in points:
                x, y = len(points) * 2, 0
                points[p1] = (x, y)
                commands.append(f"plt.scatter({x}, {y}, label='{p1}')")
                commands.append(
                    f"plt.text({x}, {y}, '{p1}', fontsize=12, ha='right')")
            if p2 not in points:
                x, y = len(points) * 2, 0
                points[p2] = (x, y)
                commands.append(f"plt.scatter({x}, {y}, label='{p2}')")
                commands.append(
                    f"plt.text({x}, {y}, '{p2}', fontsize=12, ha='right')")
            commands.append(f"draw_line({points[p1]}, {
                            points[p2]}, color='blue')")

        elif statement["type"] == "Побудувати_перпендикуляр":
            name = statement["name"]  # e.g., 'CH'
            line = statement["line"]  # e.g., 'NO'

            # Ensure the base line points are defined
            if len(line) == 2:
                base_p1, base_p2 = line[0], line[1]
                if base_p1 in points and base_p2 in points:
                    # Draw perpendicular using the base line points
                    commands.append(
                        f"draw_perpendicular('{name}', [{points[base_p1]}, {points[base_p2]}], color='red')")
                else:
                    raise ValueError(f"Line points {base_p1} or {
                                     base_p2} not defined")

    return commands
