import requests
from pytest import fixture, mark

from scanapi.template_render import _loader, render, render_body


@mark.describe("template render")
@mark.describe("render")
class TestRender:
    @fixture
    def mocked__get_template(self, mocker):
        return mocker.patch("scanapi.template_render.Environment.get_template")

    @fixture
    def mocked__request(self, mocker):
        return mocker.patch.object(requests, "PreparedRequest")

    @mark.it("should call jinja render")
    def test_should_call_jinja_render(self, mocked__get_template):
        context = {"my_context": "foo"}
        render("my_template.jinja", context)

        mocked__get_template.assert_called_once_with("my_template.jinja")
        mocked__get_template().render.assert_called_once_with(**context)

    @mark.it("should render json")
    def test_should_render_json(self, mocked__request):
        request = mocked__request()
        request.headers = {
            "Content-Length": "21",
            "Content-Type": "application/json",
        }
        request.body = b'{"name": "bulbasaur"}'
        assert '{"name": "bulbasaur"}' == render_body(request)

    @mark.it("should render plain text")
    def test_should_render_plain_text(self, mocked__request):
        request = mocked__request()
        request.headers = {
            "Content-Length": "27",
            "Content-Type": "text/plain",
        }
        request.body = b"this is a custom plain text"
        assert "this is a custom plain text" == render_body(request)

    @mark.it("should not render unsuported content type")
    def test_should_not_render_unsuported_content_type(self, mocked__request):
        request = mocked__request()
        request.headers = {
            "Content-Length": "0",
            "Content-Type": "application/octet-stream",
        }
        request.body = b""
        assert (
            "Can not render. Unsuported content type: application/octet-stream."
            == render_body(request)
        )


@mark.describe("template render")
@mark.describe("_loader")
class TestLoader:
    @mark.context("when it is external")
    @mark.it("should return file system loader")
    def test_return_file_system_loader(self):
        loader = _loader(True)

        assert loader.__class__.__name__ == "FileSystemLoader"
        assert loader.searchpath == ["./"]

    @mark.context("when it is not external")
    @mark.it("should return package loader")
    def test_return_package_loader(self):
        loader = _loader(False)
        assert loader.__class__.__name__ == "PackageLoader"
        assert loader.package_path == "templates"
