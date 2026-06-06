import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpp
import pandas as pd


def get_data(overwrite=False):
    data = pd.DataFrame({
        'height (cm)': [4.7, -5.1, 4.2, -7.6, 4.9],
        'weight (kg)': [2.9, -11.5, 8.9, -3.9, -7.9]
    })
    return data


def draw_vector(v, color='k', lstyle='-', label=None, ax=None):

    if ax is None:
        ax = plt.gca()

    # Center axes and set axes limits
    axlim = max(np.abs(v))          # axes limits
    format_axes(ax, axlim)

    # Vector parameters
    v0 = np.zeros(2)                        # vector origin
    lwidth = 2.0                            # arrow tail line width
    head_length = .1 * max(ax.get_xlim())   # arrow head length
    head_width = head_length / 3            # arrow head width

    # Draw arrow tail
    ax.plot(*list(zip(v0, 0.95 * v)), color=color, linestyle=lstyle, zorder=0)

    # Calculate head coordinates
    vperp = np.array([-v[1], v[0]]) / np.linalg.norm(v)
    head_base = v - head_length * v / np.linalg.norm(v)
    head_coords = [
        v,
        head_base + head_width * vperp,
        head_base - head_width * vperp
    ]

    # Draw arrow head
    head = mpp.Polygon(head_coords, closed=False, color=color, zorder=1)
    ax.add_patch(head)

    # Add vector labels
    if label is not None:
        ax.text(v[0], v[1], f'$\\mathbf{{{label}}}$', color=color, fontsize=15,
                ha='left' if v[0] > 0 else 'right',  # horizontal text alignment
                va='bottom' if v[1] > 0 else 'top'  # vertical text alignment
                )


def format_axes(ax, axlim, axlw=0.5, zorder=-1):

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

    # Change axes zorder
    ax.spines['left'].set_zorder(zorder)
    ax.spines['bottom'].set_zorder(zorder)


def draw_vector_list(vector_list, color_list=None, ax=None):

    if ax is None:
        ax = plt.gca()

    if color_list is None:
        color_list = mpl.cm.ScalarMappable(cmap='Dark2').to_rgba(np.linspace(0, 1, len(vector_list)))

    # Plot largest vector first to set up axes
    vector_norms = [np.linalg.norm(v) for v in vector_list]
    for i, c in zip(np.argsort(vector_norms)[::-1], color_list):
        draw_vector(vector_list[i], color=c, ax=ax)


def draw_vector_pair(u, v, ax=None):
    if ax is None:
        ax = plt.gca()
    draw_vector_list([u, v], ["0.5", "0.8"], ax=ax)
    draw_angle([u, v], ax=ax)


def draw_angle(vectors, ax, arc_color='b', fontsize=10):
    angles = np.rad2deg([np.arctan(v[1] / v[0]) + np.pi * (v[0] < 0) for v in vectors])
    arc_radius = 0.6 * min([np.linalg.norm(v) for v in vectors])
    arc = mpp.Arc((0, 0), arc_radius, arc_radius, 0, min(angles), max(angles), color=arc_color, linewidth=0.5, zorder=0)
    ax.add_patch(arc)
    if fontsize is not None:
        textpad = 0.7
        ax.text(textpad * arc_radius * np.cos(np.deg2rad(np.mean(angles))), textpad * arc_radius * np.sin(np.deg2rad(np.mean(angles))),
                f"$\\theta = {np.abs(np.diff(angles))[0]: .1f}^o$", color=arc_color, fontsize=fontsize, ha='left', va='bottom', zorder=100)
