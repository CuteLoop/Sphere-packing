import matplotlib.pyplot as plt
from viz import plot_shape
from make_shape import make_polygon, make_circle

fig, ax = plt.subplots()

polygon = make_polygon([(1, 1), (5, 1), (5, 4), (1, 4)])
circle = make_circle(center=(3, 2), radius=6, num_points=200)

plot_shape(ax, polygon, facecolor='blue', alpha=0.4)
plot_shape(ax, circle, edgecolor='red', linewidth=2)

ax.set_aspect('equal')
ax.set_title("Polygon + Circle")

plt.savefig("figs/circle_polygon.png", dpi=200, bbox_inches="tight")
plt.close()
