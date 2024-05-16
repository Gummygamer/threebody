from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color
from kivy.core.window import Window
import numpy as np
import random

class Body:
    """Represents a celestial body in the three-body simulation."""
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

class ThreeBodySimulation(Widget):
    """Widget to visualize the three-body problem simulation."""
    G = 1  # Gravitational constant
    DRAG_RADIUS = 40  # Increase the radius within which a body can be dragged
    BODY_SIZE = 20  # Increase the visual size of the bodies
    SCALE_MARGIN = 0.3  # Zoom out margin factor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the celestial bodies with more randomness in positions
        random_margin = 100  # Adjust this value to change randomness
        self.bodies = [
            Body(10, [random.uniform(150, 250), random.uniform(250, 350)], [0.3, -0.2]),
            Body(20, [random.uniform(350, 450), random.uniform(250, 350)], [-0.3, 0.2]),
            Body(30, [random.uniform(250, 350), random.uniform(450, 550)], [0.1, -0.4])
        ]
        self.dt = 1  # Time step for the simulation
        self.traces = [[] for _ in self.bodies]  # To store traces of each body
        self.dragging_body = None
        self.prev_touch_position = None
        self.scale_factor = 1
        self.colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.bind(size=self.update_canvas, pos=self.update_canvas)

        Clock.schedule_interval(self.update_simulation, 1 / 60.0)

    def gravitational_force(self, body1, body2):
        """Calculate the gravitational force exerted on body1 by body2."""
        r_vec = body2.position - body1.position
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            return np.zeros(2)
        force = self.G * body1.mass * body2.mass / r_mag ** 2
        return force * r_vec / r_mag

    def update_positions_velocities(self):
        """Update positions and velocities using the Euler method."""
        if not self.dragging_body:
            forces = [np.zeros(2, dtype=np.float64) for _ in self.bodies]

            for i, body1 in enumerate(self.bodies):
                for j, body2 in enumerate(self.bodies):
                    if i != j:
                        forces[i] += self.gravitational_force(body1, body2)

            for i, body in enumerate(self.bodies):
                acceleration = forces[i] / body.mass
                body.velocity += acceleration * self.dt
                body.position += body.velocity * self.dt
                self.traces[i].append(tuple(body.position))

    def update_simulation(self, dt):
        """Update simulation periodically."""
        self.update_positions_velocities()
        self.update_canvas()

    def update_canvas(self, *args):
        """Redraw canvas with updated positions."""
        self.canvas.clear()
        # Scale the positions to fit the screen with a margin
        x_min = min(body.position[0] for body in self.bodies)
        x_max = max(body.position[0] for body in self.bodies)
        y_min = min(body.position[1] for body in self.bodies)
        y_max = max(body.position[1] for body in self.bodies)

        width = self.width
        height = self.height

        x_range = max(x_max - x_min, 1) * (1 + self.SCALE_MARGIN)
        y_range = max(y_max - y_min, 1) * (1 + self.SCALE_MARGIN)

        x_scale = width / x_range
        y_scale = height / y_range

        self.scale_factor = min(x_scale, y_scale)

        def scale_position(position):
            return (
                (position[0] - x_min) * self.scale_factor,
                (position[1] - y_min) * self.scale_factor
            )

        with self.canvas:
            for i, body in enumerate(self.bodies):
                Color(*self.colors[i])
                pos = scale_position(body.position)
                Ellipse(pos=(pos[0] - self.BODY_SIZE // 2, pos[1] - self.BODY_SIZE // 2), size=(self.BODY_SIZE, self.BODY_SIZE))
                for trace in self.traces[i]:
                    t_pos = scale_position(trace)
                    Ellipse(pos=(t_pos[0] - 2, t_pos[1] - 2), size=(4, 4))

    def on_touch_down(self, touch):
        """Handle touch down events to initiate dragging."""
        scaled_touch = self.scale_down(touch.pos)
        for body in self.bodies:
            if np.linalg.norm(body.position - scaled_touch) < self.DRAG_RADIUS:
                self.dragging_body = body
                self.prev_touch_position = np.array(scaled_touch, dtype=np.float64)
                return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        """Handle touch move events to drag a body."""
        if self.dragging_body:
            scaled_touch = self.scale_down(touch.pos)
            movement = np.array(scaled_touch, dtype=np.float64) - self.prev_touch_position
            self.dragging_body.position += movement
            self.prev_touch_position = np.array(scaled_touch, dtype=np.float64)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """Handle touch up events to stop dragging and reset velocity."""
        if self.dragging_body:
            self.dragging_body.velocity = np.array([0, 0], dtype=np.float64)  # Set velocity to zero
            self.dragging_body = None
            return True
        return super().on_touch_up(touch)

    def scale_down(self, position):
        """Scale down screen coordinates to simulation coordinates."""
        x_min = min(body.position[0] for body in self.bodies)
        x_max = max(body.position[0] for body in self.bodies)
        y_min = min(body.position[1] for body in self.bodies)
        y_max = max(body.position[1] for body in self.bodies)

        width = self.width
        height = self.height

        x_range = max(x_max - x_min, 1) * (1 + self.SCALE_MARGIN)
        y_range = max(y_max - y_min, 1) * (1 + self.SCALE_MARGIN)

        x_scale = width / x_range
        y_scale = height / y_range

        scale_factor = min(x_scale, y_scale)

        return (
            position[0] / scale_factor + x_min,
            position[1] / scale_factor + y_min
        )

class ThreeBodyApp(App):
    def build(self):
        Window.size = (2400, 1080)
        return ThreeBodySimulation()

if __name__ == '__main__':
    ThreeBodyApp().run()