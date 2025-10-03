from tests.server.component_test_app.components.component_test_app.should_render_testing import ShouldRenderComponent


def test_should_render_true():
    assert ShouldRenderComponent(should_render=True).render().strip() == "howdy"


def test_should_render_false():
    assert ShouldRenderComponent(should_render=False).render() == ""
