from tests.server.component_test_app.components.component_test_app.should_render_testing import ShouldRenderComponent
from tests.server.component_test_app.components.component_test_app.debug_testing import DebugComponent


def test_should_render_true():
    assert ShouldRenderComponent(should_render=True).render().strip() == "howdy"


def test_should_render_false():
    assert ShouldRenderComponent(should_render=False).render() == ""


def test_debug_render_includes_start_and_end_comments(settings):
    settings.DEBUG = True
    cls_name = "DebugComponent"
    file_path = "/workspaces/django-template-component/tests/server/component_test_app/components/component_test_app/debug_testing.py"
    expected_output = f"""
<!-- START COMPONENT class: {cls_name} file: {file_path} -->
howdy

<!-- END COMPONENT class: {cls_name} file: {file_path} -->
""".lstrip()
    assert DebugComponent().render() == expected_output


def test_non_debug_render_omits_start_end_comments(settings):
    settings.DEBUG = False
    assert DebugComponent().render().strip() == "howdy"
