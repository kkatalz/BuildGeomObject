import matplotlib.pyplot as plt
import numpy as np


def draw_line(point1, point2, color='blue'):
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    plt.plot(x_values, y_values, color=color, linestyle='-', marker='o')


def draw_perpendicular(name, base_line, color='red'):
    # Extract the base line points
    base_p1, base_p2 = base_line
    # Extract characters for labeling
    lower_point, high_point = name[0], name[1]

    # Find the point on the base line where perpendicular intersects (point H)
    h_x = (base_p1[0] + base_p2[0]) / 2  # Midpoint of the base line
    h_y = base_p1[1]  # Y-coordinate of the base line
    h_point = (h_x, h_y)

    # Calculate the length of the base line
    base_length = np.sqrt(
        (base_p2[0] - base_p1[0])**2 + (base_p2[1] - base_p1[1])**2)

    # Set point C above H, with length of CH equal to half of the base line length
    c_point = (h_x, h_y + base_length / 2)

    # Draw the perpendicular segment CH
    plt.plot([h_point[0], c_point[0]], [h_point[1], c_point[1]],
             color=color, linestyle='-', marker='o')

    # Plot points C and H with labels
    plt.scatter(h_point[0], h_point[1], color='orange', label=high_point)
    plt.scatter(c_point[0], c_point[1], color='purple', label=lower_point)

    # Position labels
    plt.text(h_point[0], h_point[1] - 0.1, high_point,
             fontsize=12, ha='center', va='top')
    plt.text(c_point[0], c_point[1], lower_point,
             fontsize=12, ha='left', va='bottom')


if __name__ == "__main__":
    plt.figure(figsize=(10, 6))
    # Test the functions
    base_point1 = (0, 0)
    base_point2 = (4, 0)
    draw_line(base_point1, base_point2, color='blue')
    draw_perpendicular((2, 2), [base_point1, base_point2], color='red')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.title("Geometric Construction")
    plt.show()
