from django_template_component import TemplateComponent, register_component


@register_component("component_test_app/debug_testing")
class DebugComponent(TemplateComponent):
    template_name = "component_test_app/debug_testing.html"

    def get_context(self):
        return {}
