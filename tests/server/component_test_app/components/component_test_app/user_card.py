from django_template_component import TemplateComponent, register_component


@register_component("component_test_app/user_card")
class UserCardComponent(TemplateComponent):
    template_name = "component_test_app/user_card.html"

    def __init__(self, *, user, viewer):
        self.user = user
        self.viewer = viewer

    def get_context(self):
        return {"user": self.user, "viewer": self.viewer}
