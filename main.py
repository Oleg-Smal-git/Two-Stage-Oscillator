import math

import graphics
import physics

if __name__ == '__main__':
    graphics.Simulation(
        oscillator=physics.Oscillator(
            inner_body=physics.PointOscillatorBody(
                mass=1.0,
                shaft_length=100.0,
                position=math.pi / 4,
            ),
            outer_body=physics.PointOscillatorBody(
                mass=1.0,
                shaft_length=100.0,
                position=3 * math.pi / 8,
            )
        )
    ).run()
