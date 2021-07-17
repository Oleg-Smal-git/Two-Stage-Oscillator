import pyglet
import math
import config
import physics


class Simulation:
    def __init__(self, oscillator=physics.Oscillator()):
        if isinstance(oscillator, physics.Oscillator):
            self.oscillator = oscillator
            self.window = pyglet.window.Window(fullscreen=True)
        else:
            raise TypeError(f"Incompatible argument type: {type(oscillator)}")

    def draw(self, origin=physics.Vector()):
        if isinstance(origin, physics.Vector):
            absolute_inner_body_position = physics.Vector(
                x=math.cos(self.oscillator.inner_body.position - math.pi / 2) *
                self.oscillator.inner_body.shaft_length + origin.x,
                y=math.sin(self.oscillator.inner_body.position - math.pi / 2) *
                self.oscillator.inner_body.shaft_length + origin.y
            )

            absolute_outer_body_position = physics.Vector(
                x=math.cos(self.oscillator.outer_body.position - math.pi / 2) *
                self.oscillator.outer_body.shaft_length,
                y=math.sin(self.oscillator.outer_body.position - math.pi / 2) *
                self.oscillator.outer_body.shaft_length
            ) + absolute_inner_body_position

            pyglet.shapes.Line(
                x=origin.x,
                y=origin.y,
                x2=absolute_inner_body_position.x,
                y2=absolute_inner_body_position.y,
                width=1,
                color=(255, 0, 0)
            ).draw()

            pyglet.shapes.Line(
                x=absolute_inner_body_position.x,
                y=absolute_inner_body_position.y,
                x2=absolute_outer_body_position.x,
                y2=absolute_outer_body_position.y,
                width=1,
                color=(0, 255, 0)
            ).draw()

            pyglet.shapes.Circle(
                x=absolute_inner_body_position.x,
                y=absolute_inner_body_position.y,
                radius=3,
                color=(255, 0, 0)
            ).draw()

            pyglet.shapes.Circle(
                x=absolute_outer_body_position.x,
                y=absolute_outer_body_position.y,
                radius=3,
                color=(0, 255, 0)
            ).draw()

            pyglet.shapes.Circle(
                x=origin.x,
                y=origin.y,
                radius=3,
                color=(255, 255, 255)
            ).draw()

        else:
            raise TypeError(f"Incompatible argument type: {type(origin)}")

    def update(self, dt):
        self.window.clear()
        for _ in range(config.CONSTANTS["calculation_scale"]):
            self.oscillator.step(1 / (config.CONSTANTS["framerate"] * config.CONSTANTS["calculation_scale"]))
        self.draw(
            origin=physics.Vector(
                x=self.window.width / 2,
                y=self.window.height / 2
            )
        )

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1 / config.CONSTANTS["framerate"])
        pyglet.app.run()
