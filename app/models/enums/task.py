from enum import Enum


class StationDirection(int, Enum):
    forward = 1  # Gidiş
    backward = 2  # Dönüş


class LeafletDirection(int, Enum):
    forward = 1  # Gidiş
    backward = 2  # Dönüş
