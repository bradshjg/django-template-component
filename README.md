# django-template-component
Explicit contracts for "including" other templates within a template inspired by https://github.com/github/view_component.

A framework for building reusable, testable & encapsulated template components in Django.

## Motivation

Django supports the [`include` template tag](https://docs.djangoproject.com/en/3.2/ref/templates/builtins/#include) for
including other templates within templates.

This allows several awesome features:

* We can create reusable sub-templates that can be included in multiple pages.
* With a bit of work, we can test these templates in isolation.
* With the right invocation, we can be explicit about the context with which it will be rendered (e.g. `{% include "name_snippet.html" with greeting="Hi" only %}`).
* It supports any object with a `render` method, allowing us to include compiled `Template`s.

Template components can be thought of as a much more opinionated `include`:

* They generate tags and require explicit context (e.g. `{% name_component greeting="Hi" %}`).
* Every component is its own class to separate the business logic from the display logic.
* There is explicit testing support using `TemplateComponentTest`.

But this is probably best served by an example.

### Simple Example

We want to show a card with user details in multiple places on the site. In the simple case
there's minimal benefit to using a component, but also minimal overhead. We have an explicit


#### Using `include`

`example_user_details.html`
```
...
{% include 'user_card.html' %}
...
```

`example_user_list.html`
```
...
{% for user in users %}
  {% include 'user_card.html' with user=user only %}
{% endfor %}
...
```

`user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me</p>
  <p>{{ user.email }}</p>
</div>
```

#### Using a Template Component

`example_user_details.html`
```
...
{% user_card_component user=user %}
...
```

`example_user_list.html`
```
...
{% for user in users %}
  {% user_card_component user=user %}
{% endfor %}
...
```

`myapp/components/user_card.py`

```python
class UserCardComponent(TemplateComponent)
    template = 'user_card.html'

    def __init__(self, *, user):
      self.user = user
```

`user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me</p>
  <p>{{ user.email }}</p>
</div>
```

### Full Example

Requirements have changed and now we only want to show contact info for users that have either
opted-in to sharing that or if the user viewing that card is a staff user.

#### Using `include`

`example_user_details.html`
```
...
{% include 'user_card.html' %}
...
```

`example_user_list.html`
```
...
{% for user in users %}
  {% include 'user_card.html' with user=user only %}
{% endfor %}
...
```

`user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me</p>
  {% if user.profile.show_contact_info or viewer.is_staff %}
    <p>{{ user.email }}</p>
  {% endif %}
</div>
```

This was a pretty quick change, but it has a subtle bug. We've created an implicit reliance
on the `viewer` being passed in the context and in `example_user_list.html` we were being
explicit about the context we were passing so staff users won't be able to see contact info
unless we either pass viewer explicitly there or relax the requirements of being explicit.

#### Using a Template Component

Since there's now some business logic regarding the contact info, we can create a
component for that and encapsulate that logic in the component class. This allows us
to test the component in isolation. Additionally, since all contracts are explicit we
would've caught the earlier bug easily during testing (as it would've thrown an exception
rather than been coerced silently to an empty string).

`example_user_details.html`
```
...
{% user_card_component user=user viewer=viewer %}
...
```

`example_user_list.html`
```
...
{% for user in users %}
  {% user_card_component user=user viewer=viewer %}
{% endfor %}
...
```

`myapp/components/user_card.py`

```python
class UserCardComponent(TemplateComponent)
    template = 'user_card_component.html'

    def __init__(self, *, user, viewer):
      self.user = user
      self.viewer = viewer
```

`user_card_component.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me</p>
  {% user_contact_info_component %}
</div>
```

`myapp/components/user_contact_info.py`

```python
class UserContactInfoComponent(TemplateComponent)
    template = 'user_contact_info_component.html'

    def __init__(self, *, user, viewer):
      self.user = user
      self.viewer = viewer

    def should_render(self):
      if user.profile.show_contact_info or viewer.is_staff:
        return True
      return False
```

> Note: `should_render` is a feature of `TemplateComponent`s. The base class always returns `True` and
subclasses can choose to override this method to control whether the component should be rendered.

`user_contact_info_component.html`

```
<p>{{ user.email }}</p>
```

## Testing

### Using `include`

Django's [`testing tools`](https://docs.djangoproject.com/en/3.2/topics/testing/tools/) for templates
are largely built around testing views. If we want to test `include`d templates in isolation it's
possible but fraught for several reasons:

* It's non-obvious to set up the Django template rendering machinery (but it's not bad
once you know where to look).
* Implicit contracts are allowed, so subtle bugs can creep in depending on how other templates
`include` them. Explicit contracts are possible only if callers are careful to always pass `only`.

```python
from django.template.loader import render_to_string

class UserCardTest(SimpleTestCase):

    def test_contact_info_not_shown_if_user_opted_out(self):
        user = test_user()  # this returns a user object opted-out of sharing contact info
        context = {'user': user, 'viewer': user})
        rendered_template = render_to_string('user_card.html', context)
        self.assertInHTML('<p>test@test.com</p>', rendered_template, count=0)

    def test_contact_info_shown_if_user_opted_out_but_viewer_is_staff(self):
        user = test_user()  # this returns a user object opted-out of sharing contact info
        viwer = staff_user()
        context = {'user': user, 'viewer': viewer}
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<p>test@test.com</p>', rendered_template, count=1)
```

### Using Template Components

TODO
