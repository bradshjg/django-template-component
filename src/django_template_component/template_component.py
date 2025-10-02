from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping

from django.template.loader import get_template

if TYPE_CHECKING:
    from django.utils.safestring import SafeText


class TemplateComponent(ABC):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def template_name(self) -> str:
        pass

    @property
    @abstractmethod
    def context(self) -> Mapping[str, Any]:
        pass

    def render(self) -> SafeText | str:
        template = get_template(self.template_name)
        template.render(self.context)

    def should_render() -> bool:
        return True
