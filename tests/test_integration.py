import http

import pytest
from bs4 import BeautifulSoup
from django.template.exceptions import TemplateSyntaxError

from django_template_component.registry import ComponentNotRegisteredError


def test_user_card_template_happy_path(client):
    resp = client.get("/template/")
    assert resp.status_code == http.HTTPStatus.OK

    html = BeautifulSoup(resp.content, "html.parser")
    assert html.p.string == "jack's profile"


def test_user_card_component_happy_path(client):
    resp = client.get("/component/")
    assert resp.status_code == http.HTTPStatus.OK

    html = BeautifulSoup(resp.content, "html.parser")
    assert html.p.string == "jack's profile"


def test_valid(client):
    resp = client.get("/component-testing/valid_minimal/")
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.content.decode().strip() == "<p>howdy</p>"


def test_invalid_kwargs(client):
    with pytest.raises(TypeError, match="unexpected keyword argument 'foo'"):
        client.get("/component-testing/error_invalid_kwargs/")


def test_invalid_syntax(client):
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'msg'"):
        client.get("/component-testing/error_invalid_syntax/")


def test_component_not_registered(client):
    with pytest.raises(
        ComponentNotRegisteredError, match="Component 'component_test_app/non-existent' is not registered"
    ):
        client.get("/component-testing/error_nonexistent_component/")


def test_invalid_unquoted_component_name(client):
    with pytest.raises(TemplateSyntaxError, match="'component' tag's template name should be in quotes"):
        client.get("/component-testing/error_unquoted_component_name/")


def test_valid_but_weird_syntax(client):
    # we currently leverage Django's kwargs parser for templatetag tokens...it gives up when it stops seeing
    # key=val constructs...it's weird but we should test it to preserve that behavior.
    #
    # TODO: a more opinionated parser is probably a good idea right?
    resp = client.get("/component-testing/valid_but_weird_syntax/")
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.content.decode().strip() == "<p>howdy</p>"
