import pytest
import jinja2

from scanapi.template_render import render, _loader


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
