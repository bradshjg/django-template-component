from django_template_component.test import render_component

from bs4 import BeautifulSoup


def test_render_component_valid_component():
    rendered_component = render_component('component_test_app/minimal', msg="howdy")

    html = BeautifulSoup(rendered_component, 'html.parser')
    assert html.p.string == "howdy"
