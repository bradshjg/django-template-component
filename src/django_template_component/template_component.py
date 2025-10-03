from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping

from django import template

from django_template_component.loader import ComponentLoader

if TYPE_CHECKING:
    from django.utils.safestring import SafeText


class TemplateComponent(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    @abstractmethod
    def template_name(self) -> str:
        pass

    @abstractmethod
    def get_context(self) -> Mapping[str, Any]:
        pass

    @property
    def template_loader(self) -> ComponentLoader:
        if hasattr(TemplateComponent, "_template_loader"):
            return TemplateComponent._template_loader

        TemplateComponent._template_loader = ComponentLoader(template.engine.Engine.get_default())
        return TemplateComponent._template_loader

    def render(self) -> SafeText | str:
        if not self.should_render():
            return ""
        component_template = self.template_loader.get_template(self.template_name)
        component_context = template.Context(self.get_context())
        return component_template.render(component_context)

    def should_render(self) -> bool:
        return True
