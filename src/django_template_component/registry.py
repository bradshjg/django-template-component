from __future__ import annotations


class ComponentNotRegisteredError(Exception):
    def __init__(self, name):
        message = f"Component '{name}' is not registered"
        super().__init__(message)


class ComponentRegistry:
    def __init__(self):
        self._registry: dict[str, type] = {}

    def register(self, *, name: str, component: type):
        self._registry[name] = component

    def get(self, name):
        if name not in self._registry:
            raise ComponentNotRegisteredError(name)

        return self._registry[name]

    def clear(self):
        self._registry = {}


component_registry = ComponentRegistry()


def register_component(name: str):
    def decorator(component: type):
        component_registry.register(name=name, component=component)
        return component

    return decorator
