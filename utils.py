import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from carla.planner.map import CarlaMap


def plot_trajectories(trajectory_dict, title, add_legend=True):
    """
    Plots a set of trajectories on CARLA Town 01
    inputs: trajectory_dict and title of plot
    example:
    trajectory_dict = {'baseline' : {'x' : [0,1,2], 'y' [3,4,5]}}
    Each key of the dictionary will correspond to the label for that trajectory
    and each value is a dictionary with keys 'x' and 'y' whose values are
    array-like. See supplied jupyter notebooks for more examples.
    """
    carla_map = CarlaMap('Town01_nemesis', 0.1653, 50)
    image     = mpimg.imread("carla/planner/Town01_nemesis.png")
    fig, ax   = plt.subplots(1)
    pad       = 30

    fig.set_size_inches(10, 10)
    plt.rcParams.update({'font.size': 12})
    ax.imshow(image, alpha=0.4)

    all_x_pixels = []
    all_y_pixels = []

    for label, positions in trajectory_dict.items():
        x_position = positions['x']
        y_position = positions['y']

        pixelX = []
        pixelY = []
        for i in range(len(x_position)):
            pixel = carla_map.convert_to_pixel([x_position[i], y_position[i], 0])
            pixelX.append(pixel[0])
            pixelY.append(pixel[1])
            all_x_pixels.append(pixel[0])
            all_y_pixels.append(pixel[1])

        if len(x_position) == 1:
            plt.scatter(pixelX[0], pixelY[0], label=label, s=500)
        else:
            if label.lower() == 'baseline':
                plt.plot(pixelX, pixelY, linestyle='dashed', label=label, color='k',markersize=12, linewidth=4)
            else:
                plt.plot(pixelX, pixelY,linestyle='dashed', label=label, color='blue',markersize=12, linewidth=4)

    xmin = np.maximum(0, min(all_x_pixels) - pad)
    xmax = np.minimum(image.shape[1], max(all_x_pixels) + pad)
    ymin = np.maximum(0, min(all_y_pixels) - pad)
    ymax = np.minimum(image.shape[0], max(all_y_pixels) + pad)
    plt.axis([xmin, xmax, ymax, ymin])
    plt.title(title)
    if add_legend:
        plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    return plt
