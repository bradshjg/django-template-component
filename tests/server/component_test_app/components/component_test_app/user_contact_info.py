from django_template_component import register, TemplateComponent


@register('user_contact_info')
class UserContactInfoComponent(TemplateComponent):
    template_name = 'myapp/user_contact_info.html'

    def __init__(self, *, user, viewer):
      self.user = user
      self.viewer = viewer

    def should_render(self):
      if self.user.profile.show_contact_info or self.viewer.is_staff:
        return True
      return False
