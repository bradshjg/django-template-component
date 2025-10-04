import http

import pytest
from bs4 import BeautifulSoup
from django.template.exceptions import TemplateSyntaxError


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


def test_valid_variable(client):
    resp = client.get("/component-testing/valid_minimal/", data={"msg": "howdy-variable"})
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.content.decode().strip() == "<p>howdy-variable</p>"


def test_valid_literal(client):
    resp = client.get("/component-testing/valid_minimal/")
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.content.decode().strip() == "<p>howdy-literal</p>"


def test_invalid_kwargs(client):
    with pytest.raises(TemplateSyntaxError, match="error instantiating component") as e:
        client.get("/component-testing/error_invalid_kwargs/")
    assert "got an unexpected keyword argument 'foo'" in str(e.value.__cause__)


def test_component_not_registered(client):
    with pytest.raises(TemplateSyntaxError, match="error resolving component") as e:
        client.get("/component-testing/error_nonexistent_component/")
    assert "Component 'component_test_app/non-existent' is not registered" in str(e.value.__cause__)


def test_invalid_unquoted_component_name(client):
    with pytest.raises(TemplateSyntaxError, match="'component' tag's template name should be in quotes"):
        client.get("/component-testing/error_unquoted_component_name/")


def test_invalid_syntax(client):
    with pytest.raises(TemplateSyntaxError, match="'component' tag requires 'key=value' arguments"):
        client.get("/component-testing/error_invalid_syntax/")
