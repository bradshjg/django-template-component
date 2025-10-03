# django-template-component
Explicit contracts for "including" other templates within a template inspired by https://github.com/github/view_component.

A framework for building reusable, testable, and encapsulated template components in Django.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Motivation](#motivation)
- [Examples](#examples)
- [License](#license)

## Installation

`pip install django-template-component`

### Setup

Add `django-template-component` to `INSTALLED_APPS`.

This will import `{app}/components/**/*.py` files to run the registration hooks. Be careful of import-time side effects in those files!

## Usage

### Anatomy of a Template Component

Templates components, similar to templates, are placed within Django app directories under a `components/{app_name}/` folder.

An example layout:

```
my_app/
|  apps.py
|  ...
|__components/
|  |__my_app/
|     |  demo.py
|     |  demo.html
|     |  ...
|__templates/
   |__my_app/
      |  demo.html
      |  ...
```

#### Component class

Components should inherit from `django_template_component.TemplateComponent` and provide a

* `template_name` variable - the loader will look for a component's template with this name (i.e. it searches `components/` folders, not `templates/` folders)
* `get_context()` method - return a dictionary that defines the context available to the component's template

Components can also provide an optional

* `should_render()` method - return a boolean indicating whether the component should be rendered (defaults to `True`)

Component must register themselves under a name, by convention namespaced by app.

`my_app/components/my_app/demo.py`
```python
from django_template_component import TemplateComponent, register_component


@register_component("my_app/demo")
class DemoComponent(TemplateComponent):
    template_name = "my_app/demo.html"

    def __init__(self, *, msg):
        self.msg = msg

    def get_context(self):
        return {"msg": self.msg}
```

### Component template

Component templates only have access to the context returned by the component's `get_context()` method.

`my_app/components/my_app/demo.html`
```html
<p>{{ msg }}</p>
```

### Using a component in a Django template

Rendering a component in a template uses the `component` template tag, supplying a quoted component name and any number of `key=value`
arguments that will be supplied as keyword arguments to initialize the component class. These values follow the template language
variable evaluation rules, and passing either variables or literals is supported.

`my_app/templates/my_app/demo.hml`
```
{% load component %}

{% component 'my_app/demo' msg='howdy' %}
```

which will render

```html
<p>howdy</p>
```

## Testing

`django_template_component.test.render_component` will render a registered component, accepting arbitrary kwargs.

```python
from django_template_component.test import render_component
from django.test import SimpleTestCase

class UserCardTest(SimpleTestCase):
    def test_contact_info_not_shown_if_user_opted_out(self):
        user = test_user(opt_out=True)
        anon = test_user()
        rendered_component = render_component('myapp/user_card', user=user, viewer=anon)
        self.assertInHTML('test@test.com', rendered_template, count=0)

    def test_contact_info_shown_if_user_opted_out_but_viewer_is_staff(self):
        user = test_user(opt_out=True)
        staff = staff_user()
        rendered_template = render_component('myapp/user_card', user=user, viewer=staff)
        self.assertInHTML('test@test.com', rendered_template, count=1)
```

## Motivation

Django supports the [`include` template tag](https://docs.djangoproject.com/en/3.2/ref/templates/builtins/#include) for
including other templates within templates.

This allows several awesome features:

* We can create reusable sub-templates that can be included in multiple pages.
* With a bit of work, we can test these templates in isolation.
* With the right invocation, we can be explicit about the context with which it will be rendered (e.g. `{% include "name_snippet.html" with greeting="Hi" only %}`).
* It supports any object with a `render` method, allowing us to `include` compiled `Template`s.

Template components can be thought of as a much more opinionated `include`:

* They require explicit context (e.g. `{% component 'name' greeting="Hi" %}`).
* Every component is its own class to separate the business logic from the display logic.

But this is probably best served by an example.

### Differences from Rails View Components

There is no support for "slots", meaning that all render context is included via the `component` template tag. This is an intentional
design decision...but not one without drawbacks. This library intends to provide support for decomposing documents into testable and
shareable components. It does not intend to provide the necessary tooling to build a design system. Components can render componens,
but there's no rich support for callers modifying the rendering process. In Django, libraries like
[django-viewcomponent](https://github.com/rails-inspire-django/django-viewcomponent) exist with that goal in mind.

## Examples

### Simple Example

We want to show a card with user details in multiple places on the site. In the simple case
there's minimal benefit to using a component, but also minimal overhead.

#### Using `include`

`myapp/templates/myapp/example_user_details.html`
```
...
{% include 'myapp/user_card.html' %}
...
```

`myapp/templates/myapp/example_user_list.html`
```
...
{% for user in users %}
  {% include 'myapp/user_card.html' with user=user only %}
{% endfor %}
...
```

`myapp/templates/myapp/user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me }}</p>
  <p>{{ user.email }}</p>
</div>
```

#### Using a Template Component

`myapp/templates/myapp/example_user_details.html`
```
...
{% component 'myapp/user_card' user=user %}
...
```

`myapp/templates/myapp/example_user_list.html`
```
...
{% for user in users %}
  {% component 'myapp/user_card' user=user %}
{% endfor %}
...
```

`myapp/components/my_app/user_card.py`

```python
from django_template_component import register_component, TemplateComponent


@register_component('my_app/user_card')
class UserCardComponent(TemplateComponent):
    template_name = 'my_app/user_card.html'

    def __init__(self, *, user):
      self.user = user

    def get_context(self):
        return {"user": self.user}
```

`myapp/components/my_app/user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me }}</p>
  <p>{{ user.email }}</p>
</div>
```

### Full Example

Requirements have changed and now we only want to show contact info for users that have either
opted-in to sharing that or if the user viewing that card is a staff user.

#### Using `include`

`myapp/templates/myapp/example_user_details.html`
```
...
{% include 'myapp/user_card.html' %}
...
```

`myapp/templates/myapp/example_user_list.html`
```
...
{% for user in users %}
  {% include 'myapp/user_card.html' with user=user only %}
{% endfor %}
...
```

`myapp/templates/myapp/user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me }}</p>
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

`myapp/templates/myapp/example_user_details.html`
```
...
{% component 'myapp/user_card' user=user viewer=viewer %}
...
```

`myapp/templates/myapp/example_user_list.html`
```
...
{% for user in users %}
  {% component 'myapp/user_card' user=user viewer=viewer %}
{% endfor %}
...
```

`myapp/components/myapp/user_card.py`

```python
from django_template_component import register_component, TemplateComponent


@register_component('my_app/user_card')
class UserCardComponent(TemplateComponent):
    template_name = 'myapp/user_card.html'

    def __init__(self, *, user, viewer):
      self.user = user
      self.viewer = viewer

    def get_context(self):
      return {"user": self.user, "viewer": self.viewer}
```

`myapp/components/myapp/user_card.html`
```
<div class="card">
  <img src="{{ user.profile.avatar_url }}" alt="{{ user.get_full_name }}">
  <p>{{ user.profile.title }}</p>
  <p>{{ user.profile.about_me }}</p>
  {% component 'user_contact_info' user=user viewer=viewer %}
</div>
```

`myapp/components/myapp/user_contact_info.py`

```python
from django_template_component import register_component, TemplateComponent


@register_component('my_app/user_contact_info')
class UserContactInfoComponent(TemplateComponent):
    template_name = 'myapp/user_contact_info.html'

    def __init__(self, *, user, viewer):
      self.user = user
      self.viewer = viewer

    def get_context(self):
      return {"user": self.user, "viewer": self.viewer}

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

## License

`django-template-component` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
