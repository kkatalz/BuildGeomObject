import matplotlib.pyplot as plt
import numpy as np


def draw_line(point1, point2, color='blue'):
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    plt.plot(x_values, y_values, color=color, linestyle='-', marker='o')


def draw_perpendicular(point, base_line, color='red'):
    # Extract the base line points
    base_p1, base_p2 = base_line

    # Find the point on base line where perpendicular intersects (point H)
    # For a horizontal line, this is directly below/above point C
    h_x = (base_p1[0] + base_p2[0]) / 2  # midpoint of base line
    h_y = base_p1[1]  # y-coordinate of base line
    h_point = (h_x, h_y)

    # Calculate the length of the base line
    base_length = np.sqrt(
        (base_p2[0] - base_p1[0])**2 + (base_p2[1] - base_p1[1])**2)

    # Set point C above H, with length of CH equal to half of base line length
    c_point = (h_x, h_y + base_length / 2)

    # Draw the perpendicular segment CH
    plt.plot([h_point[0], c_point[0]], [h_point[1], c_point[1]],
             color=color, linestyle='-', marker='o')

    # Plot points C and H with labels in legend
    plt.scatter(h_point[0], h_point[1], color='orange', label='H')
    plt.scatter(c_point[0], c_point[1], color='purple', label='C')

    # Position H label slightly below the line
    plt.text(h_point[0], h_point[1] - 0.1, 'H',
             fontsize=12, ha='center', va='top')
    plt.text(c_point[0], c_point[1], 'C',
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
