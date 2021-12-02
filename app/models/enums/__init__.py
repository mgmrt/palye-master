from enum import Enum


class Status(int, Enum):
    active = 1
    passive = 0
    deleted = -1


class State(int, Enum):
    approved = 1
    waiting = 0
    declined = -1
