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
            commands.append(f"draw_line({points[p1]}, {points[p2]})")

        elif statement["type"] == "Побудувати_перпендикуляр":
            name = statement["name"]
            line = statement["line"]

            # Extract points of the perpendicular segment
            perp_p1, perp_p2 = name[0], name[1]

            # Get or create points for the base line
            if len(line) == 2:
                base_p1, base_p2 = line[0], line[1]

                # If base line points don't exist, we need to get them from points dictionary
                if base_p1 in points and base_p2 in points:
                    base_start = points[base_p1]
                    base_end = points[base_p2]

                    # Calculate midpoint of base line
                    mid_x = (base_start[0] + base_end[0]) / 2
                    mid_y = (base_start[1] + base_end[1]) / 2

                    # Calculate perpendicular points
                    # First point will be on the base line
                    points[perp_p1] = (mid_x, mid_y)
                    # Second point will be above/below depending on the case
                    points[perp_p2] = (mid_x, mid_y + 1)  # 1 unit up

                    # Plot the points
                    commands.append(
                        f"plt.scatter({mid_x}, {mid_y}, label='{perp_p1}')")
                    commands.append(f"plt.text({mid_x}, {mid_y}, '{
                                    perp_p1}', fontsize=12, ha='right')")
                    commands.append(
                        f"plt.scatter({mid_x}, {mid_y + 1}, label='{perp_p2}')")
                    commands.append(
                        f"plt.text({mid_x}, {mid_y + 1}, '{perp_p2}', fontsize=12, ha='right')")

                    # Draw the perpendicular line
                    commands.append(
                        f"draw_line({points[perp_p1]}, {points[perp_p2]})")
                else:
                    raise ValueError(f"Line points {base_p1} or {
                                     base_p2} not defined")

    return commands
