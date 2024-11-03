# graphics.py: файл для реалізації функцій побудови графічних елементів.
import matplotlib.pyplot as plt
import numpy as np


def draw_line(point1, point2):
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    plt.plot(x_values, y_values, 'bo-')


def draw_perpendicular(segment, line):
    # Extract the base line points
    p1, p2 = line

    # Find the midpoint of AB
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2

    # Set point H at the midpoint
    h_point = (mid_x, mid_y)

    # Calculate the length of AB
    ab_length = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    # Set point C above H, with length of CH equal to half of AB
    c_point = (mid_x, mid_y + ab_length / 2)

    # Draw the perpendicular segment CH
    plt.plot([h_point[0], c_point[0]], [h_point[1], c_point[1]], 'r-')

    # Plot points C and H with labels for the legend
    plt.scatter(h_point[0], h_point[1], color='orange', label='H')
    plt.scatter(c_point[0], c_point[1], color='purple', label='C')

    # Position H label slightly below the line
    plt.text(h_point[0], h_point[1] - 0.1, 'H',
             fontsize=12, ha='center', va='top')
    plt.text(c_point[0], c_point[1], 'C', fontsize=12, ha='left', va='bottom')


if __name__ == "__main__":
    plt.figure()
    draw_line((0, 0), (4, 0))
    draw_perpendicular((2, 0), [(0, 0), (4, 0)])
    plt.show()
