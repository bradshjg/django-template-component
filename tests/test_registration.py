import pytest

from django_template_component import TemplateComponent
from django_template_component.registry import ComponentNotRegisteredError, component_registry


def test_component_successful_registration():
    component = component_registry.get("component_test_app/user_card")
    assert issubclass(component, TemplateComponent)


def test_component_does_not_exist_error():
    with pytest.raises(ComponentNotRegisteredError, match="Component 'non-existent' is not registered"):
        component_registry.get("non-existent")
