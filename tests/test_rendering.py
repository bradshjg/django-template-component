import http

from bs4 import BeautifulSoup


def test_template(client):
    resp = client.get("/template/")
    assert resp.status_code == http.HTTPStatus.OK

    html = BeautifulSoup(resp.content, "html.parser")
    assert html.p.string == "jack's profile"


def test_component(client):
    resp = client.get("/component/")
    assert resp.status_code == http.HTTPStatus.OK

    html = BeautifulSoup(resp.content, "html.parser")
    assert html.p.string == "jack's profile"

