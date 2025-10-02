import pytest

from django_template_component import TemplateComponent
from django_template_component.registry import component_registry, ComponentNotRegistered

def test_component_successfuL_registration():
    component = component_registry.get('component_test_app/user_card')
    assert issubclass(component, TemplateComponent)

def test_component_does_not_exist_error():
    with pytest.raises(ComponentNotRegistered, match='Component "non-existent" is not registered'):
        component_registry.get('non-existent')
