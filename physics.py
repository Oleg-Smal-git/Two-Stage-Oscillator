import math
import config


class Vector:
    def __init__(self, x=0.0, y=0.0):
        if (
                (isinstance(x, int) or isinstance(x, float)) and
                (isinstance(y, int) or isinstance(y, float))
        ):
            self.x = x
            self.y = y
        else:
            raise TypeError(f"Incompatible argument types: x: {type(x)}, y: {type(y)}")

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(
                x=self.x + other.x,
                y=self.y + other.y
            )
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(
                x=self.x - other.x,
                y=self.y - other.y
            )
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(
                x=self.x * other,
                y=self.y * other
            )
        elif isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(
                x=self.x / other,
                y=self.y / other
            )

    def __copy__(self):
        new = type(self)()
        new.__dict__.update(self.__dict__)
        return new

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __isub__(self, other):
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __idiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def length(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def angle(self, other):
        if isinstance(other, Vector):
            return math.acos((self * other) / (self.length() * other.length()))
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")


class PointOscillatorBody:
    def __init__(self, mass=0.0, shaft_length=0.0, position=0.0, velocity=0.0, acceleration=0.0):
        if (
            (isinstance(shaft_length, int) or isinstance(shaft_length, float)) and
            (isinstance(mass, int) or isinstance(mass, float)) and
            (isinstance(position, int) or isinstance(position, float)) and
            (isinstance(velocity, int) or isinstance(velocity, float)) and
            (isinstance(acceleration, int) or isinstance(acceleration, float))
        ):
            self.shaft_length = shaft_length
            self.mass = mass
            self.position = position
            self.velocity = velocity
            self.acceleration = acceleration
        else:
            raise TypeError(
                f"Incompatible argument types: " +
                f"mass: {type(mass)}, position: {type(position)}, " +
                f"velocity: {type(velocity)}, acceleration: {type(acceleration)}"
            )

    def step(self, delta_time=0.0):
        if isinstance(delta_time, int) or isinstance(delta_time, float):
            self.position += self.velocity * delta_time + self.acceleration * math.pow(delta_time, 2) / 2
            self.velocity += self.acceleration * delta_time
        else:
            raise TypeError(f"Incompatible argument type: {type(delta_time)}")


class Oscillator:
    def __init__(self, inner_body=PointOscillatorBody(), outer_body=PointOscillatorBody()):
        if (
            isinstance(inner_body, PointOscillatorBody) and
            isinstance(outer_body, PointOscillatorBody)
        ):
            self.inner_body = inner_body
            self.outer_body = outer_body
        else:
            raise TypeError(
                f"Incompatible argument types: " +
                f"inner_body: {type(inner_body)}, outer_body: {type(outer_body)}"
            )

    def calculate_acceleration(self):
        self.inner_body.acceleration =\
            (
                -config.CONSTANTS["gravitational_acceleration"] *
                (2 * self.inner_body.mass + self.outer_body.mass) *
                math.sin(self.inner_body.position) -

                config.CONSTANTS["gravitational_acceleration"] *
                self.outer_body.mass *
                math.sin(self.inner_body.position - 2 * self.outer_body.position) -

                2 * math.sin(self.inner_body.position - self.outer_body.position) *
                self.outer_body.mass *
                (
                    math.pow(self.outer_body.velocity, 2) * self.outer_body.shaft_length +
                    math.pow(self.inner_body.velocity, 2) * self.inner_body.shaft_length *
                    math.cos(self.inner_body.position - self.outer_body.position)
                )
            ) /\
            (
                self.inner_body.shaft_length * (
                    2 * self.inner_body.mass + self.outer_body.mass - self.outer_body.mass *
                    math.cos(2 * self.inner_body.position - 2 * self.outer_body.position)
                )
            ) -\
            self.inner_body.velocity * config.CONSTANTS["dampening"]

        self.outer_body.acceleration =\
            (
                2 * math.sin(self.inner_body.position - self.outer_body.position) *
                (
                    math.pow(self.inner_body.velocity, 2) *
                    self.inner_body.shaft_length *
                    (self.inner_body.mass + self.outer_body.mass) +

                    config.CONSTANTS["gravitational_acceleration"] *
                    (self.inner_body.mass + self.outer_body.mass) *
                    math.cos(self.inner_body.position) +

                    math.pow(self.outer_body.velocity, 2) *
                    self.outer_body.shaft_length * self.outer_body.mass *
                    math.cos(self.inner_body.position - self.outer_body.position)
                )
            ) /\
            (
                self.outer_body.shaft_length * (
                    2 * self.inner_body.mass + self.outer_body.mass - self.outer_body.mass *
                    math.cos(2 * self.inner_body.position - 2 * self.outer_body.position)
                )
            ) -\
            self.outer_body.velocity * config.CONSTANTS["dampening"]

    def step(self, delta_time=0.0):
        if isinstance(delta_time, int) or isinstance(delta_time, float):
            self.calculate_acceleration()
            self.inner_body.step(delta_time=delta_time)
            self.inner_body.position = max(
                self.inner_body.position - 2 * math.pi,
                self.inner_body.position
            )
            if self.inner_body.position < 0:
                self.inner_body.position += 2 * math.pi

            self.outer_body.step(delta_time=delta_time)
            self.outer_body.position = max(
                self.outer_body.position - 2 * math.pi,
                self.outer_body.position
            )
            if self.outer_body.position < 0:
                self.outer_body.position += 2 * math.pi
        else:
            raise TypeError(f"Incompatible argument type: {type(delta_time)}")
