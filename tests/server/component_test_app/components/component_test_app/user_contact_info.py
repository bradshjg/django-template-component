from django_template_component import TemplateComponent, register_component


@register_component("component_test_app/user_contact_info")
class UserContactInfoComponent(TemplateComponent):
    template_name = "component_test_app/user_contact_info.html"

    def __init__(self, *, user, viewer):
        self.user = user
        self.viewer = viewer

    def get_context(self):
        return {"user": self.user, "viewer": self.viewer}

    def should_render(self):
        if self.user.profile.show_contact_info or self.viewer.is_staff:
            return True
        return False
