from typing import Type

class ComponentNotRegistered(Exception):
    def __init__(self, name):
        message = f'Component "{name}" is not registered'
        super().__init__(message)


class ComponentRegistry:
    def __init__(self):
        self._registry: dict[str, Type] = {}

    def register(self, *, name: str, component: Type):
        self._registry[name] = component

    def get(self, name):
        if name not in self._registry:
            raise ComponentNotRegistered(name)

        return self._registry[name]

    def clear(self):
        self._registry = {}

component_registry = ComponentRegistry()


def register_component(name: str):
    def decorator(component: Type):
        component_registry.register(name=name, component=component)
        return component

    return decorator
