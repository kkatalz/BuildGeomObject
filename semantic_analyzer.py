def semantic_analysis(parsed_tree):
    commands = []
    points = {}
    segments = []

    # First pass: collect all segments
    def collect_segments(node):
        if node.value.startswith("Sentence (Побудувати_відрізок)"):
            identifier_pair = node.children[0]
            point_list = extract_points(identifier_pair)
            if len(point_list) >= 2:
                segments.append((point_list[0], point_list[1]))
        elif node.value.startswith("Sentence (Перетин_відрізків)"):
            line1_pair = node.children[0]
            line2_pair = node.children[2]
            line1_points = extract_points(line1_pair)
            line2_points = extract_points(line2_pair)
            if len(line1_points) >= 2:
                segments.append((line1_points[0], line1_points[1]))
            if len(line2_points) >= 2:
                segments.append((line2_points[0], line2_points[1]))
        for child in node.children:
            collect_segments(child)

    def extract_points(identifier_pair):
        points = []
        for child in identifier_pair.children:
            identifier = child.value.split(': ')[1]
            current_point = ""
            for i, char in enumerate(identifier):
                if i == 0:
                    current_point = char
                elif char.isdigit():
                    current_point += char
                else:
                    if current_point:
                        points.append(current_point)
                    current_point = char
            if current_point:
                points.append(current_point)
        return points

    # First collect all segments
    collect_segments(parsed_tree)

    def point_in_any_segment(point_name):
        return any(point_name in segment for segment in segments)

    def process_node(node):
        if node.value.startswith("Sentence (Позначити_точку)"):
            point_name = node.children[0].value.split(': ')[1]
            coordinates_node = node.children[0].children[0] if node.children[0].children else None

            # Check if point is part of any segment BEFORE processing coordinates
            if point_in_any_segment(point_name):
                print(f"You can't assign coordinates for point '{
                      point_name}' as it exists in a 'Відрізок'. Using default values instead.")
                x, y = len(points) * 2, 0
            elif coordinates_node:
                x, y = map(float, coordinates_node.value.split(
                    ': ')[1].strip('()').split(','))
            else:
                x, y = len(points) * 2, 0

            if point_name not in points:
                points[point_name] = (x, y)
                commands.append(f"plt.scatter({x}, {y}, label='{point_name}')")
                commands.append(
                    f"plt.text({x}, {y}, '{point_name}', fontsize=12, ha='right')")
            else:
                print(f"Point {point_name} already exists. Skipping.")

        elif node.value.startswith("Sentence (Побудувати_відрізок)"):
            identifier_pair = node.children[0]
            point_list = extract_points(identifier_pair)
            if len(point_list) >= 2:
                p1, p2 = point_list[0], point_list[1]  # Take first two points
                segments.append((p1, p2))

                for p in [p1, p2]:
                    if p not in points:
                        x, y = len(points) * 2, 0
                        points[p] = (x, y)
                        commands.append(f"plt.scatter({x}, {y}, label='{p}')")
                        commands.append(
                            f"plt.text({x}, {y}, '{p}', fontsize=12, ha='right')")
                commands.append(f"draw_line({points[p1]}, {
                                points[p2]}, color='blue')")
            else:
                print(f"Not enough points to draw a line: {point_list}")

        elif node.value.startswith("Sentence (Побудувати_перпендикуляр)"):
            perp_pair = node.children[0]
            line_pair = node.children[2]
            perp_points = extract_points(perp_pair)
            line_points = extract_points(line_pair)

            if len(line_points) >= 2 and len(perp_points) >= 2:
                base_p1, base_p2 = line_points[0], line_points[1]
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
                        commands.append(f"plt.text({start_x}, {start_y}, '{
                                        perp_start}', fontsize=12, ha='right')")
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
                    commands.append(f"plt.text({end_x}, {end_y}, '{
                                    perp_end}', fontsize=12, ha='right')")
                else:
                    print(
                        f"Point {perp_end} in 'перпендикуляр' already exists. Skipping.")

                # Draw the perpendicular line
                commands.append(f"draw_line({points[perp_start]}, {
                                points[perp_end]}, color='red')")
            else:
                print(f"Not enough points to draw a perpendicular: {
                      perp_points} to {line_points}")

        elif node.value.startswith("Sentence (Перетин_відрізків)"):
            line1_pair = node.children[0]
            line2_pair = node.children[2]
            line1_points = extract_points(line1_pair)
            line2_points = extract_points(line2_pair)

            if len(line1_points) >= 2 and len(line2_points) >= 2:
                p1, p2 = line1_points[0], line1_points[1]
                p3, p4 = line2_points[0], line2_points[1]

                # Get the existing points for the second line (CJ)
                if p3 in points and p4 in points:
                    x3, y3 = points[p3]
                    x4, y4 = points[p4]

                    # Calculate a point that will definitely intersect
                    mid_x = (x3 + x4) / 2
                    mid_y = y3  # Since it's horizontal

                    # Place the first point of KL
                    if p1 not in points:
                        # Changed from 2 to 1
                        points[p1] = (mid_x - 1, mid_y + 1)
                        commands.append(
                            f"plt.scatter({mid_x - 1}, {mid_y + 1}, label='{p1}')")
                        commands.append(
                            f"plt.text({mid_x - 1}, {mid_y + 1}, '{p1}', fontsize=12, ha='right')")

                    # Place the second point of KL
                    if p2 not in points:
                        # Changed from 2 to 1
                        points[p2] = (mid_x + 1, mid_y - 1)
                        commands.append(
                            f"plt.scatter({mid_x + 1}, {mid_y - 1}, label='{p2}')")
                        commands.append(
                            f"plt.text({mid_x + 1}, {mid_y - 1}, '{p2}', fontsize=12, ha='right')")

                    # Draw the intersecting lines
                    commands.append(f"draw_line({points[p1]}, {
                                    points[p2]}, color='blue')")

                else:
                    print(f"POINTS {p3} OR {p4} IN ВІДРІЗОК {
                          p3 + p4} ARE NOT DEFINED")

        for child in node.children:
            process_node(child)

    process_node(parsed_tree)

    return commands
