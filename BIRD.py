import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import numpy as np

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = 0.00001
        self.velocity_y = 0.00001
        self.line, = ax.plot([], [], 'go')

    def update(self, x, y):
        self.x = x
        self.y = y
        self.line.set_data([self.x], [self.y])

    def align(self, dots):
        """Align with the average heading of the flock."""
        if len(dots) > 0:
            avg_velocity_x = np.mean([dot.velocity_x for dot in dots])
            avg_velocity_y = np.mean([dot.velocity_y for dot in dots])
            self.velocity_x += (avg_velocity_x - self.velocity_x) * 0.0001
            self.velocity_y += (avg_velocity_y - self.velocity_y) * 0.0001

    def cohesion(self, dots):
        """Move towards the center of mass of the flock."""
        if len(dots) > 0:
            avg_x = np.mean([dot.x for dot in dots])
            avg_y = np.mean([dot.y for dot in dots])
            distance_x = avg_x - self.x
            distance_y = avg_y - self.y
            self.velocity_x += distance_x * 0.0001
            self.velocity_y += distance_y * 0.0001

    def separation(self, dots):
        """Avoid collisions with nearby flockmates."""
        for dot in dots:
            if dot is not self:
                distance_x = dot.x - self.x
                distance_y = dot.y - self.y
                distance = np.sqrt(distance_x**2 + distance_y**2)
                if distance < 0.5:
                    self.velocity_x += distance_x * 0.0001 / distance
                    self.velocity_y += distance_y * 0.0001 / distance

fig, ax = plt.subplots(figsize=(15,8))
ax.plot(1,1,1)
ax.set_xlim(0, 15)  # Set the x-axis limits
ax.set_ylim(0, 10) 

# plt init pos
np.random.seed(0)  # for reproducibility
dots = []
for i in range(20):
    x = np.random.uniform(0, 14)
    y = np.random.uniform(0, 9)
    dot = Dot(x, y)
    dots.append(dot)

# update anim func
def update_movement(frame):
    for dot in dots:
        dot.separation(dots)
        dot.align(dots)
        dot.cohesion(dots)
        x = dot.x + dot.velocity_x
        y = dot.y + dot.velocity_y
        
        if x >= 14.9 or x <= 0:
            dot.velocity_x *= -1
        if y >= 9.8 or y <= 0:
            dot.velocity_y *= -1
        
        dot.update(x, y)
    return dots

# anim func
ani = FuncAnimation(fig, update_movement, frames=100, interval=50)

# fig settings
# Set the major locators of the x and y axes to integer values
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.grid(False)

# show
plt.show()