import os
import numpy as np
from scipy.linalg import sqrtm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpp
import pandas as pd


def plot_vector(v, color='k', label=None, ax=None):

    if ax is None:
        ax = plt.gca()

    # Vector parameters
    axlim = max(np.abs(v))          # axes limits
    lwidth = 2.0                    # arrow tail line width
    head_length = .1 * axlim        # arrow head length
    head_width = head_length / 3    # arrow head width

    # Vector origin
    v0 = np.zeros(2)

    # Draw arrow tail
    ax.plot(*list(zip(v0, 0.95 * v)), color=color, zorder=-1)

    # Calculate head coordinates
    vperp = np.array([-v[1], v[0]]) / np.linalg.norm(v)
    head_base = v - head_length * v / np.linalg.norm(v)
    head_coords = [
        v,
        head_base + head_width * vperp,
        head_base - head_width * vperp
    ]

    # Draw arrow head
    head = mpp.Polygon(head_coords, closed=False, color=color)
    ax.add_patch(head)

    # Center axes and set axes limits
    format_axes(ax, axlim)

    # Add vector labels
    if label is not None:
        ax.text(v[0], v[1], f'$\\mathbf{{{label}}}$', color=color, fontsize=15,
                ha='left' if v[0] > 0 else 'right',  # horizontal text alignment
                va='bottom' if v[1] > 0 else 'top'  # vertical text alignment
                )


def format_axes(ax, axlim, axlw=0.5):

    ax.set_aspect('equal')

    # Center axes
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Axes limits (change only if necessary)
    xmin, xmax = ax.get_xlim()
    xmax = axlim if xmax < axlim else xmax
    xmin = -axlim if xmin > -axlim else xmin
    ax.set_xlim([xmin, xmax])
    ymin, ymax = ax.get_ylim()
    ymax = axlim if ymax < axlim else ymax
    ymin = -axlim if ymin > -axlim else ymin
    ax.set_ylim([ymin, ymax])

    # Change axes line width
    ax.spines['left'].set_linewidth(axlw)
    ax.spines['bottom'].set_linewidth(axlw)


def load_data():

    filename = './data/athletes.csv'

    # Load synthetic data set
    if os.path.isfile(filename):
        return pd.read_csv(filename)

    # Create synthetic data set
    else:
        N = 100
        weight, height = sqrtm(np.array([[5 ** 2, 5 ** 2], [5 ** 2, 10 ** 2]])).dot(np.random.randn(2, N))
        speed = height - weight + 5 * np.random.randn(N)
        data = pd.DataFrame({
            'weight (kg)': weight,
            'height (cm)': height,
            'speed (m/s)': speed
        })
        data.to_csv(filename, index=False)
        return data
