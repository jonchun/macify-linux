"""Spotlight Module"""
from macifylinux.components import latte_dock

components = [latte_dock]


def install(*args, **kwargs):
    for component in components:
        component.install(*args, **kwargs)


def upgrade(*args, **kwargs):
    for component in components:
        component.upgrade(*args, **kwargs)


def remove(*args, **kwargs):
    for component in components:
        component.remove(*args, **kwargs)
