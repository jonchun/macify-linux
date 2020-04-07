"""Hotkeys Module"""
from macifylinux.components import kinto

components = [kinto]


def install(*args, **kwargs):
    for component in components:
        component.install(*args, **kwargs)


def upgrade(*args, **kwargs):
    for component in components:
        component.upgrade(*args, **kwargs)


def remove(*args, **kwargs):
    for component in components:
        component.remove(*args, **kwargs)
