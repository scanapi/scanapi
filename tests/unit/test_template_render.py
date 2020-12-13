import pytest
import requests

from scanapi.template_render import _loader, render, render_body


class TestTemplateRender:
    class TestRender:
        @pytest.fixture
        def mocked__get_template(self, mocker):
            return mocker.patch("scanapi.template_render.Environment.get_template")

        def test_should_call_jinja_render(self, mocked__get_template):
            context = {"my_context": "foo"}
            render("my_template.jinja", context)

            mocked__get_template.assert_called_once_with("my_template.jinja")
            mocked__get_template().render.assert_called_once_with(**context)

        @pytest.fixture
        def mocked__request(self, mocker):
            return mocker.patch.object(requests, "PreparedRequest")

        def test_should_render_json(self, mocked__request):
            request = mocked__request()
            request.headers = {
                "Content-Length": "44",
                "Content-Type": "application/json",
            }
            request.body = b'{"uuid": "76fe526d665a46f2812ec6580dd5b34a"}'
            assert '{"uuid": "76fe526d665a46f2812ec6580dd5b34a"}' == render_body(
                request
            )

        def test_should_render_plain_text(self, mocked__request):
            request = mocked__request()
            request.headers = {"Content-Length": "35", "Content-Type": "text/plain"}
            request.body = b"this is a custom plain text"
            assert "this is a custom plain text" == render_body(request)

        def test_should_render_binary_content(self, mocked__request):
            request = mocked__request()
            request.headers = {
                "Content-Length": "0",
                "Content-Type": "application/octet-stream",
            }
            request.body = b""
            assert "Binary content" == render_body(request)

    class TestLoader:
        class TestWhenIsExternal:
            def test_return_file_system_loader(self):
                loader = _loader(True)

                assert loader.__class__.__name__ == "FileSystemLoader"
                assert loader.searchpath == ["./"]

        class TestWhenIsNotExternal:
            def test_return_package_loader(self):
                loader = _loader(False)
                assert loader.__class__.__name__ == "PackageLoader"
                assert loader.package_path == "templates"
