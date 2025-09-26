#!/usr/bin/env -S uv run --script
import dataclasses
import math
import sys
from typing import Self


class Vec3:
    e: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def __init__(self, x: float, y: float, z: float):
        self.e = (x, y, z)

    @property
    def x(self):
        return self.e[0]

    @property
    def y(self):
        return self.e[1]

    @property
    def z(self):
        return self.e[2]

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __getitem__(self, index):
        assert 0 <= index < 3
        return self.e[index]

    def __len__(self):
        return math.sqrt(self.len_squared())

    def __iadd__(self, other: Self):
        assert isinstance(other, Vec3)
        self.e[0] += other.e[0]
        self.e[1] += other.e[1]
        self.e[2] += other.e[2]
        return self

    def __imul__(self, t: float):
        assert isinstance(t, float)
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self

    def __idiv__(self, t: float):
        assert isinstance(t, float)
        return self * (1.0 / t)

    def len_squared(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __add__(self, other: Self):
        assert isinstance(other, Vec3)
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other: Self | float):
        assert isinstance(other, (Vec3, float))
        if isinstance(other, float):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, t: float):
        assert isinstance(t, float)
        return self * (1.0 / t)

    def dot(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def cross(self, other: Self):
        assert isinstance(other, Vec3)
        return Vec3(
            self.e[1] * other.e[2] - self.e[2] * other.e[1],
            self.e[2] * other.e[0] - self.e[0] * other.e[2],
            self.e[0] * other.e[1] - self.e[1] * other.e[0],
        )

    def unit_vector(self):
        return self / len(self)


class Color(Vec3):
    def write_color(self, fp=sys.stdout):
        r, g, b = color.e
        rbyte = int(255.999 * r)
        gbyte = int(255.999 * g)
        bbyte = int(255.999 * b)
        print(f"{rbyte} {gbyte} {bbyte}", file=fp)


class Point3(Vec3):
    pass


@dataclasses.dataclass
class Ray:
    origin: Point3
    direction: Vec3

    def at(self, t: float):
        return self.origin + self.direction * t


def log(msg: str, fp=sys.stderr, flush=True):
    print(msg, file=fp, flush=flush)


def ray_color(ray: Ray):
    return Color(0, 0, 0)


if __name__ == "__main__":
    aspect_ratio = 16 / 9
    image_width = 400
    image_height = h if (h := int(image_width / aspect_ratio)) >= 1 else 1
    log(f"{image_width=}, {image_height=}, {aspect_ratio=:.2f}")

    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (float(image_width) / image_height)
    camera_center = Point3(0, 0, 0)

    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = (
        camera_center - Vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
    )

    img_width = img_height = 256
    print(f"P3\n{img_width} {img_height}\n255")
    for j in range(img_height):
        log(f"Scanlines remaining: {img_height - j} ")
        for i in range(img_width):
            color = Color(float(i) / (img_width - 1), float(j) / (img_height - 1), 0)
            color.write_color()
    log("Done")
