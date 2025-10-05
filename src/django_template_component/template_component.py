from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

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
        if self.include_debug_info:
            component_template = self.wrap_with_debug_info(component_template)
        rendered_content = component_template.render(component_context)
        return rendered_content

    def wrap_with_debug_info(self, component_template: template.Template) -> template.Template:
        cls_name = self.__class__.__name__
        file_path = inspect.getsourcefile(self.__class__)
        start_comment = f"\n<!-- START COMPONENT class: {cls_name} file: {file_path} -->\n"
        end_comment = f"\n<!-- END COMPONENT class: {cls_name} file: {file_path} -->\n"
        component_template.nodelist.insert(0, template.base.TextNode(start_comment))
        component_template.nodelist.append(template.base.TextNode(end_comment))
        return component_template

    @property
    def include_debug_info(self) -> bool:
        return bool(settings.DEBUG)

    def should_render(self) -> bool:
        return True
