from django_template_component import register, TemplateComponent


@register('user_card')
class UserCardComponent(TemplateComponent):
    template_name = 'myapp/user_card.html'

    def __init__(self, *, user, viewer):
      self.user = user
      self.viewer = viewer
