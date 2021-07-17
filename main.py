import math

import graphics
import physics

if __name__ == '__main__':
    graphics.Simulation(
        oscillator=physics.Oscillator(
            inner_body=physics.PointOscillatorBody(
                mass=1.0,
                shaft_length=100.0,
                position=3 * math.pi / 2,
                velocity=1.0
            ),
            outer_body=physics.PointOscillatorBody(
                mass=2.0,
                shaft_length=100.0,
                position=3 * math.pi / 2,
                velocity=2.0
            )
        )
    ).run()
