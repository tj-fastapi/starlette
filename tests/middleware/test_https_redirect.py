from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from tests.types import TestClientFactory


def test_https_redirect_middleware(test_client_factory: TestClientFactory) -> None:
    def homepage(request: Request) -> PlainTextResponse:
        return PlainTextResponse("OK", status_code=200)

    app = Starlette(
        routes=[Route("/", endpoint=homepage)],
        middleware=[Middleware(HTTPSRedirectMiddleware)],
    )

    client = test_client_factory(app, base_url="https://testserver")
    response = client.get("/")
    assert response.status_code == 200

    client = test_client_factory(app)
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://testserver/"

    client = test_client_factory(app, base_url="http://testserver:80")
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://testserver/"

    client = test_client_factory(app, base_url="http://testserver:443")
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://testserver/"

    client = test_client_factory(app, base_url="http://testserver:123")
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://testserver:123/"
