from django_template_component import TemplateComponent, register_component


@register_component("component_test_app/minimal")
class UserCardComponent(TemplateComponent):
    template_name = "component_test_app/minimal.html"

    def __init__(self, *, msg):
        self.msg = msg

    def get_context(self):
        return {"msg": self.msg}
