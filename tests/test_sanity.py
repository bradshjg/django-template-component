import http

from bs4 import BeautifulSoup


def test_sanity():
    assert True


def test_django_sanity(client):
    resp = client.get("/")
    assert resp.status_code == http.HTTPStatus.OK

    html = BeautifulSoup(resp.content, "html.parser")

    assert html.h1.string == "Howdy"
