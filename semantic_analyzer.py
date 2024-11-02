def semantic_analysis(parsed_data):
    commands = []
    points = {}

    for statement in parsed_data:
        if statement["type"] == "Позначити_точку":
            point_name = statement["name"]
            x, y = len(points) * 2, 0  # Simple positioning
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
            commands.append(f"draw_line({points[p1]}, {points[p2]})")

        elif statement["type"] == "Побудувати_перпендикуляр":
            # For perpendicular CH to AB, we need:
            # - Point C: some distance above AB
            # - Point H: intersection point on AB
            name = statement["name"]
            line = statement["line"]

            # Calculate position for point C
            x = 2  # Position above point B
            y = 2  # 2 units up from the base line
            c_point = (x, y)

            # Store the perpendicular segment points
            points['C'] = c_point

            # Get the base line points
            if len(line) == 2:
                p1, p2 = line[0], line[1]
                if p1 in points and p2 in points:
                    commands.append(
                        f"draw_perpendicular([{c_point}], [{points[p1]}, {points[p2]}])")
                else:
                    raise ValueError(f"Line points {p1} or {p2} not defined")

    return commands
